"""Business logic for realistic order simulation workflows."""

from __future__ import annotations

import random
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import ClassVar, Dict, List, Sequence

from ..config import CUSTOMER_COUNT, END_YEAR, ORDER_COUNT, OUTPUT_FOLDER, PRODUCT_COUNT, SEED, START_YEAR
from ..constants import (
    CUSTOMER_PERSONA_DISTRIBUTION,
    CUSTOMER_PERSONA_ORDER_RANGES,
    CUSTOMER_PERSONA_PRICE_BIAS,
    CUSTOMER_PERSONA_TOP_UP_DISTRIBUTION,
    DEFAULT_MONTH_WEIGHT,
    MAX_ORDER_QUANTITY,
    ORDER_ITEM_COUNT_DISTRIBUTION,
    ORDER_STATUS_DISTRIBUTION,
    PAYMENT_METHOD_DISTRIBUTION,
    SEASONAL_MONTH_WEIGHTS,
)
from ..logger import setup_logger
from ..models.order import Order
from ..models.order_item import OrderItem
from ..models.payment import Payment
from ..utils import read_csv_rows

logger = setup_logger(__name__)

WeightedDistribution = Dict[object, float]


@dataclass(frozen=True)
class CustomerReference:
    customer_id: int
    registration_date: datetime
    address_id: int


@dataclass(frozen=True)
class ProductReference:
    product_id: int
    selling_price: float
    popularity_weight: float


@dataclass
class OrderSimulation:
    """Container for the three generated order-domain datasets."""

    orders: List[Order]
    order_items: List[OrderItem]
    payments: List[Payment]


@dataclass(frozen=True)
class OrderSimulationCacheKey:
    """Identifies a reusable order simulation for one input snapshot."""

    input_dir: Path
    target_orders: int
    customers_mtime: float | None
    products_mtime: float | None


class OrderSimulationContext:
    """Lightweight in-memory context shared by order-domain CSV generators."""

    _cache: ClassVar[dict[OrderSimulationCacheKey, OrderSimulation]] = {}

    def __init__(self, input_dir: Path | str | None = None) -> None:
        self.input_dir = Path(input_dir or OUTPUT_FOLDER)

    def get_simulation(self, target_orders: int = ORDER_COUNT) -> OrderSimulation:
        """Return one cached simulation for orders, order items, and payments."""
        cache_key = self._cache_key(target_orders)
        simulation = self._cache.get(cache_key)
        if simulation is None:
            simulation = OrderService(input_dir=self.input_dir).simulate_orders(target_orders=target_orders)
            self._cache[cache_key] = simulation
        return simulation

    @classmethod
    def clear_cache(cls) -> None:
        """Clear cached simulations; intended for tests and long-lived processes."""
        cls._cache.clear()

    def _cache_key(self, target_orders: int) -> OrderSimulationCacheKey:
        resolved_input_dir = self.input_dir.resolve()
        return OrderSimulationCacheKey(
            input_dir=resolved_input_dir,
            target_orders=target_orders,
            customers_mtime=self._mtime(resolved_input_dir / "customers.csv"),
            products_mtime=self._mtime(resolved_input_dir / "products.csv"),
        )

    def _mtime(self, path: Path) -> float | None:
        return path.stat().st_mtime if path.exists() else None


class OrderService:
    """Simulate realistic ecommerce orders and validate related datasets."""

    def __init__(self, input_dir: Path | str | None = None) -> None:
        self.input_dir = Path(input_dir or OUTPUT_FOLDER)
        self._simulation: OrderSimulation | None = None

    def simulate_orders(self, target_orders: int = ORDER_COUNT) -> OrderSimulation:
        """Generate orders, order items, and payments from one behavior model."""
        if self._simulation is not None and len(self._simulation.orders) == target_orders:
            return self._simulation

        logger.info("Generating Orders")
        rng = random.Random(SEED)
        customers = self._load_customers()
        products = self._load_products()
        plans = self._build_customer_order_plan(customers, target_orders, rng)
        product_weights_by_persona = self._product_weights_by_persona(products)

        orders: List[Order] = []
        order_items: List[OrderItem] = []
        payments: List[Payment] = []
        order_item_id = 1

        logger.info("Generating Order Items")
        logger.info("Generating Payments")
        for order_id, (customer, persona) in enumerate(plans, start=1):
            order_date = self._random_order_datetime(customer.registration_date, rng)
            order_status = self._weighted_choice(ORDER_STATUS_DISTRIBUTION, rng)
            payment_status = self._payment_status_for_order(order_status, rng)
            selected_products = self._select_products(products, product_weights_by_persona[persona], rng)
            total_amount = 0.0

            for product in selected_products:
                quantity = self._quantity_for_persona(persona, rng)
                discount = 0.0
                line_total = round(product.selling_price * quantity, 2)
                total_amount = round(total_amount + line_total, 2)
                order_items.append(
                    OrderItem(
                        order_item_id=order_item_id,
                        order_id=order_id,
                        product_id=product.product_id,
                        quantity=quantity,
                        unit_price=round(product.selling_price, 2),
                        discount_percentage=discount,
                        created_at=order_date,
                    )
                )
                order_item_id += 1

            orders.append(
                Order(
                    order_id=order_id,
                    customer_id=customer.customer_id,
                    order_date=order_date,
                    order_status=order_status,
                    payment_status=payment_status,
                    total_amount=round(total_amount, 2),
                    shipping_address_id=customer.address_id,
                    billing_address_id=customer.address_id,
                    created_at=order_date,
                )
            )
            payments.append(
                Payment(
                    payment_id=order_id,
                    order_id=order_id,
                    payment_method=self._weighted_choice(PAYMENT_METHOD_DISTRIBUTION, rng),
                    payment_date=order_date + timedelta(minutes=rng.randint(1, 45)),
                    payment_status=payment_status,
                    payment_amount=round(total_amount, 2),
                    transaction_reference=self._transaction_reference(order_id),
                    created_at=order_date,
                )
            )

        simulation = OrderSimulation(orders=orders, order_items=order_items, payments=payments)
        logger.info("Validation")
        self.validate(simulation, customers, products)
        logger.info("Completion")
        self._simulation = simulation
        return simulation

    def validate(
        self,
        simulation: OrderSimulation,
        customers: Sequence[CustomerReference] | None = None,
        products: Sequence[ProductReference] | None = None,
    ) -> None:
        """Validate foreign keys, totals, timelines, and lifecycle consistency."""
        customer_refs = {customer.customer_id: customer for customer in (customers or self._load_customers())}
        product_ids = {product.product_id for product in (products or self._load_products())}
        orders_by_id = {order.order_id: order for order in simulation.orders}
        items_by_order: Dict[int, List[OrderItem]] = {}

        for item in simulation.order_items:
            if item.order_id not in orders_by_id:
                raise ValueError(f"Invalid order_id on order item: {item.order_id}")
            if item.product_id not in product_ids:
                raise ValueError(f"Invalid product_id on order item: {item.product_id}")
            items_by_order.setdefault(item.order_id, []).append(item)

        for order in simulation.orders:
            customer = customer_refs.get(order.customer_id)
            if customer is None:
                raise ValueError(f"Invalid customer_id on order: {order.customer_id}")
            if order.order_date < customer.registration_date:
                raise ValueError(f"Order date before registration for order: {order.order_id}")
            items = items_by_order.get(order.order_id, [])
            if not items:
                raise ValueError(f"Order has no items: {order.order_id}")
            product_ids_in_order = [item.product_id for item in items]
            if len(product_ids_in_order) != len(set(product_ids_in_order)):
                raise ValueError(f"Duplicate products in order: {order.order_id}")
            item_total = round(
                sum(
                    round(item.quantity * item.unit_price * (1 - item.discount_percentage / 100), 2)
                    for item in items
                ),
                2,
            )
            if item_total != round(order.total_amount, 2):
                raise ValueError(f"Order total mismatch for order: {order.order_id}")

        seen_transactions: set[str] = set()
        for payment in simulation.payments:
            order = orders_by_id.get(payment.order_id)
            if order is None:
                raise ValueError(f"Invalid order_id on payment: {payment.order_id}")
            if round(payment.payment_amount, 2) != round(order.total_amount, 2):
                raise ValueError(f"Payment amount mismatch for order: {payment.order_id}")
            if payment.payment_status != order.payment_status:
                raise ValueError(f"Payment status mismatch for order: {payment.order_id}")
            if payment.payment_status not in self._allowed_payment_statuses(order.order_status):
                raise ValueError(f"Impossible payment status for order: {payment.order_id}")
            if payment.transaction_reference in seen_transactions:
                raise ValueError(f"Duplicate transaction reference: {payment.transaction_reference}")
            seen_transactions.add(payment.transaction_reference)

    def _build_customer_order_plan(
        self,
        customers: Sequence[CustomerReference],
        target_orders: int,
        rng: random.Random,
    ) -> List[tuple[CustomerReference, str]]:
        plans: List[tuple[CustomerReference, str]] = []
        for customer in customers:
            persona = self._weighted_choice(CUSTOMER_PERSONA_DISTRIBUTION, rng)
            minimum, maximum = CUSTOMER_PERSONA_ORDER_RANGES[persona]
            order_count = rng.randint(minimum, maximum) if maximum else 0
            plans.extend((customer, persona) for _ in range(order_count))

        if not plans:
            raise ValueError("No eligible customer orders could be generated.")

        while len(plans) < target_orders:
            customer = rng.choice(customers)
            persona = self._weighted_choice(CUSTOMER_PERSONA_TOP_UP_DISTRIBUTION, rng)
            plans.append((customer, persona))

        rng.shuffle(plans)
        return plans[:target_orders]

    def _select_products(
        self,
        products: Sequence[ProductReference],
        product_weights: Sequence[float],
        rng: random.Random,
    ) -> List[ProductReference]:
        item_count = min(self._weighted_choice(ORDER_ITEM_COUNT_DISTRIBUTION, rng), len(products))
        selected: List[ProductReference] = []
        selected_ids: set[int] = set()

        while len(selected) < item_count:
            product = rng.choices(
                population=products,
                weights=product_weights,
                k=1,
            )[0]
            if product.product_id in selected_ids:
                continue
            selected.append(product)
            selected_ids.add(product.product_id)

        return selected

    def _product_weights_by_persona(self, products: Sequence[ProductReference]) -> Dict[str, List[float]]:
        return {
            persona: [
                product.popularity_weight * max(product.selling_price, 1.0) ** (price_bias - 1)
                for product in products
            ]
            for persona, price_bias in CUSTOMER_PERSONA_PRICE_BIAS.items()
        }

    def _random_order_datetime(self, registration_date: datetime, rng: random.Random) -> datetime:
        start = max(registration_date, datetime(START_YEAR, 1, 1))
        end = datetime(END_YEAR, 12, 31, 23, 59, 59)
        if start > end:
            return start

        months = list(range(1, 13))
        month = self._weighted_choice({month: SEASONAL_MONTH_WEIGHTS.get(month, DEFAULT_MONTH_WEIGHT) for month in months}, rng)
        for _ in range(50):
            year = rng.randint(start.year, end.year)
            day = rng.randint(1, self._days_in_month(year, month))
            candidate = datetime(
                year,
                month,
                day,
                rng.randint(0, 23),
                rng.randint(0, 59),
                rng.randint(0, 59),
            )
            if start <= candidate <= end:
                return candidate

        delta_seconds = int((end - start).total_seconds())
        return start + timedelta(seconds=rng.randint(0, max(delta_seconds, 0)))

    def _load_customers(self) -> List[CustomerReference]:
        path = self.input_dir / "customers.csv"
        if not path.exists():
            return [
                CustomerReference(
                    customer_id=index,
                    registration_date=datetime(START_YEAR, 1, 1),
                    address_id=index,
                )
                for index in range(1, CUSTOMER_COUNT + 1)
            ]

        customers: List[CustomerReference] = []
        for row in read_csv_rows(path):
            registration_date = datetime.strptime(row["registration_date"], "%Y-%m-%d")
            customers.append(
                CustomerReference(
                    customer_id=int(row["customer_id"]),
                    registration_date=registration_date,
                    address_id=int(row.get("address_id") or row["customer_id"]),
                )
            )
        return customers

    def _load_products(self) -> List[ProductReference]:
        path = self.input_dir / "products.csv"
        if not path.exists():
            return self._synthetic_products()

        raw_products: List[tuple[int, float]] = []
        for row in read_csv_rows(path):
            price = row.get("selling_price") or row.get("price") or "100.00"
            raw_products.append((int(row["product_id"]), float(price)))
        if not raw_products:
            return self._synthetic_products()
        return self._with_popularity_weights(raw_products)

    def _synthetic_products(self) -> List[ProductReference]:
        raw_products = [(index, float(100 + (index % 5000))) for index in range(1, PRODUCT_COUNT + 1)]
        return self._with_popularity_weights(raw_products)

    def _with_popularity_weights(self, raw_products: Sequence[tuple[int, float]]) -> List[ProductReference]:
        products_by_price = sorted(raw_products, key=lambda item: item[1], reverse=True)
        total = len(products_by_price)
        top_cutoff = max(1, int(total * 0.10))
        next_cutoff = max(top_cutoff + 1, int(total * 0.30))

        weighted_products: List[ProductReference] = []
        for index, (product_id, price) in enumerate(products_by_price):
            if index < top_cutoff:
                segment_weight = 0.50 / top_cutoff
            elif index < next_cutoff:
                segment_weight = 0.30 / max(next_cutoff - top_cutoff, 1)
            else:
                segment_weight = 0.20 / max(total - next_cutoff, 1)
            weighted_products.append(
                ProductReference(
                    product_id=product_id,
                    selling_price=round(price, 2),
                    popularity_weight=segment_weight,
                )
            )
        return weighted_products

    def _payment_status_for_order(self, order_status: str, rng: random.Random) -> str:
        if order_status in {"Delivered", "Shipped", "Packed"}:
            return "Success"
        if order_status == "Pending":
            return "Pending"
        if order_status == "Returned":
            return "Refunded"
        return rng.choice(["Failed", "Refunded"])

    def _transaction_reference(self, order_id: int) -> str:
        reference_uuid = uuid.uuid5(uuid.NAMESPACE_URL, f"techmart-payment-{order_id}")
        return f"TXN-{order_id:012d}-{reference_uuid}"

    def _allowed_payment_statuses(self, order_status: str) -> set[str]:
        if order_status in {"Delivered", "Shipped", "Packed"}:
            return {"Success"}
        if order_status == "Pending":
            return {"Pending"}
        if order_status == "Returned":
            return {"Refunded"}
        if order_status == "Cancelled":
            return {"Failed", "Refunded"}
        return {"Failed", "Refunded"}

    def _quantity_for_persona(self, persona: str, rng: random.Random) -> int:
        if persona == "vip":
            return rng.choices([1, 2, 3, 4], weights=[0.25, 0.35, 0.25, 0.15], k=1)[0]
        if persona == "premium":
            return rng.choices([1, 2, 3, 4], weights=[0.45, 0.30, 0.18, 0.07], k=1)[0]
        return rng.randint(1, MAX_ORDER_QUANTITY)

    def _weighted_choice(self, distribution: WeightedDistribution, rng: random.Random):
        return rng.choices(
            population=list(distribution.keys()),
            weights=list(distribution.values()),
            k=1,
        )[0]

    def _days_in_month(self, year: int, month: int) -> int:
        if month == 12:
            return 31
        first_next_month = datetime(year, month + 1, 1)
        return (first_next_month - timedelta(days=1)).day
