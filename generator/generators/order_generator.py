from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from ..config import ORDER_COUNT
from ..logger import setup_logger
from ..models.order import Order
from ..services.order_service import OrderSimulationContext
from ..utils import ensure_output_dir, write_csv

logger = setup_logger(__name__)


class OrderGenerator:
    def __init__(self, output_dir: Path | str | None = None) -> None:
        self.output_dir = ensure_output_dir(output_dir)
        self._context = OrderSimulationContext(input_dir=self.output_dir)

    def generate(self, count: int = ORDER_COUNT) -> List[Dict[str, Any]]:
        logger.info("Generating Orders")
        simulation = self._context.get_simulation(target_orders=count)
        rows = [self._to_row(order) for order in simulation.orders]
        logger.info("CSV Writing")
        write_csv(self.output_dir / "orders.csv", rows)
        logger.info("Orders generated: %s", len(rows))
        return rows

    def _to_row(self, order: Order) -> Dict[str, Any]:
        return {
            "order_id": order.order_id,
            "customer_id": order.customer_id,
            "order_date": order.order_date.strftime("%Y-%m-%d %H:%M:%S"),
            "order_status": order.order_status,
            "payment_status": order.payment_status,
            "total_amount": order.total_amount,
            "shipping_address_id": order.shipping_address_id,
            "billing_address_id": order.billing_address_id,
        }
