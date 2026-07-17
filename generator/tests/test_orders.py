"""Tests for the order simulation engine."""

from __future__ import annotations

import csv
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from generator.generators.order_generator import OrderGenerator
from generator.generators.order_item_generator import OrderItemGenerator
from generator.generators.payment_generator import PaymentGenerator
from generator.services.order_service import OrderService, OrderSimulationContext


def test_order_service_generates_valid_related_datasets(tmp_path: Path) -> None:
    _write_reference_csvs(tmp_path)

    simulation = OrderService(input_dir=tmp_path).simulate_orders(target_orders=75)

    assert len(simulation.orders) == 75
    assert len(simulation.payments) == 75
    assert len(simulation.order_items) >= 75

    customers = _customer_registration_dates(tmp_path)
    products = set(range(1, 31))
    items_by_order = defaultdict(list)
    for item in simulation.order_items:
        items_by_order[item.order_id].append(item)
        assert item.product_id in products

    for order in simulation.orders:
        assert order.customer_id in customers
        assert order.order_date >= customers[order.customer_id]
        items = items_by_order[order.order_id]
        assert 1 <= len(items) <= 5
        assert len({item.product_id for item in items}) == len(items)
        expected_total = round(
            sum(
                round(item.quantity * item.unit_price * (1 - item.discount_percentage / 100), 2)
                for item in items
            ),
            2,
        )
        assert order.total_amount == expected_total

    payments_by_order = {payment.order_id: payment for payment in simulation.payments}
    assert len({payment.transaction_reference for payment in simulation.payments}) == 75
    for order in simulation.orders:
        payment = payments_by_order[order.order_id]
        assert payment.payment_amount == order.total_amount
        assert payment.payment_status == order.payment_status
        assert payment.payment_status in _allowed_payment_statuses(order.order_status)


def test_order_generators_write_consistent_csvs(tmp_path: Path) -> None:
    _write_reference_csvs(tmp_path)

    orders = OrderGenerator(output_dir=tmp_path).generate(count=40)
    order_items = OrderItemGenerator(output_dir=tmp_path).generate(order_count=40)
    payments = PaymentGenerator(output_dir=tmp_path).generate(order_count=40)

    assert len(orders) == 40
    assert len(payments) == 40
    assert len(order_items) >= 40

    loaded_orders = _read_csv(tmp_path / "orders.csv")
    loaded_items = _read_csv(tmp_path / "order_items.csv")
    loaded_payments = _read_csv(tmp_path / "payments.csv")

    assert len(loaded_orders) == 40
    assert len(loaded_payments) == 40
    assert len(loaded_items) == len(order_items)

    order_totals = {int(order["order_id"]): float(order["total_amount"]) for order in loaded_orders}
    item_totals = defaultdict(float)
    seen_products_by_order = defaultdict(set)
    for item in loaded_items:
        order_id = int(item["order_id"])
        product_id = int(item["product_id"])
        assert product_id not in seen_products_by_order[order_id]
        seen_products_by_order[order_id].add(product_id)
        item_totals[order_id] += round(
            int(item["quantity"])
            * float(item["unit_price"])
            * (1 - float(item["discount_percentage"]) / 100),
            2,
        )

    for order_id, order_total in order_totals.items():
        assert round(item_totals[order_id], 2) == order_total

    for payment in loaded_payments:
        order_id = int(payment["order_id"])
        assert float(payment["payment_amount"]) == order_totals[order_id]


def test_order_generators_share_one_simulation_context(tmp_path: Path, monkeypatch) -> None:
    _write_reference_csvs(tmp_path)
    OrderSimulationContext.clear_cache()
    original_simulate_orders = OrderService.simulate_orders
    call_count = 0

    def counted_simulate_orders(self, target_orders: int = 100000):
        nonlocal call_count
        call_count += 1
        return original_simulate_orders(self, target_orders=target_orders)

    monkeypatch.setattr(OrderService, "simulate_orders", counted_simulate_orders)

    OrderGenerator(output_dir=tmp_path).generate(count=25)
    OrderItemGenerator(output_dir=tmp_path).generate(order_count=25)
    PaymentGenerator(output_dir=tmp_path).generate(order_count=25)

    assert call_count == 1


def _write_reference_csvs(tmp_path: Path) -> None:
    customer_rows = [
        {
            "customer_id": index,
            "registration_date": f"2021-{(index % 9) + 1:02d}-01",
            "address_id": index,
        }
        for index in range(1, 26)
    ]
    product_rows = [
        {
            "product_id": index,
            "selling_price": 100 + index * 25,
        }
        for index in range(1, 31)
    ]
    _write_csv(tmp_path / "customers.csv", customer_rows)
    _write_csv(tmp_path / "products.csv", product_rows)


def _write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _customer_registration_dates(tmp_path: Path) -> dict[int, datetime]:
    return {
        int(row["customer_id"]): datetime.strptime(row["registration_date"], "%Y-%m-%d")
        for row in _read_csv(tmp_path / "customers.csv")
    }


def _allowed_payment_statuses(order_status: str) -> set[str]:
    if order_status in {"Delivered", "Shipped", "Packed"}:
        return {"Success"}
    if order_status == "Pending":
        return {"Pending"}
    if order_status == "Returned":
        return {"Refunded"}
    return {"Failed", "Refunded"}
