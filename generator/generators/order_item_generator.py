from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from ..config import MAX_ITEMS_PER_ORDER, ORDER_COUNT, PRODUCT_COUNT
from ..logger import setup_logger
from ..utils import ensure_output_dir, write_csv

logger = setup_logger(__name__)


class OrderItemGenerator:
    def __init__(self, output_dir: Path | str | None = None) -> None:
        self.output_dir = ensure_output_dir(output_dir)

    def generate(self) -> List[Dict[str, Any]]:
        logger.info("Generating order items...")
        rows: List[Dict[str, Any]] = []
        order_item_id = 1
        for order_id in range(1, ORDER_COUNT + 1):
            item_count = 1 + (order_id % MAX_ITEMS_PER_ORDER)
            for _ in range(item_count):
                rows.append(
                    {
                        "order_item_id": order_item_id,
                        "order_id": order_id,
                        "product_id": (order_item_id % PRODUCT_COUNT) + 1,
                        "quantity": (order_item_id % 5) + 1,
                        "unit_price": round(100 + (order_item_id % 1000), 2),
                        "discount_percentage": round((order_item_id % 10) * 0.5, 2),
                    }
                )
                order_item_id += 1

        write_csv(self.output_dir / "order_items.csv", rows)
        logger.info("Order items generated: %s", len(rows))
        return rows
