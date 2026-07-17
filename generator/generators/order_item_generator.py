from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from ..config import ORDER_COUNT
from ..logger import setup_logger
from ..models.order_item import OrderItem
from ..services.order_service import OrderSimulationContext
from ..utils import ensure_output_dir, write_csv

logger = setup_logger(__name__)


class OrderItemGenerator:
    def __init__(self, output_dir: Path | str | None = None) -> None:
        self.output_dir = ensure_output_dir(output_dir)
        self._context = OrderSimulationContext(input_dir=self.output_dir)

    def generate(self, order_count: int = ORDER_COUNT) -> List[Dict[str, Any]]:
        logger.info("Generating Order Items")
        simulation = self._context.get_simulation(target_orders=order_count)
        rows = [self._to_row(item) for item in simulation.order_items]
        logger.info("CSV Writing")
        write_csv(self.output_dir / "order_items.csv", rows)
        logger.info("Order items generated: %s", len(rows))
        return rows

    def _to_row(self, item: OrderItem) -> Dict[str, Any]:
        return {
            "order_item_id": item.order_item_id,
            "order_id": item.order_id,
            "product_id": item.product_id,
            "quantity": item.quantity,
            "unit_price": item.unit_price,
            "discount_percentage": item.discount_percentage,
        }
