from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from ..config import INVENTORY_COUNT, PRODUCT_COUNT
from ..logger import setup_logger
from ..utils import ensure_output_dir, write_csv

logger = setup_logger(__name__)


class InventoryGenerator:
    def __init__(self, output_dir: Path | str | None = None) -> None:
        self.output_dir = ensure_output_dir(output_dir)

    def generate(self) -> List[Dict[str, Any]]:
        logger.info("Generating inventory...")
        rows: List[Dict[str, Any]] = []
        for index in range(1, INVENTORY_COUNT + 1):
            rows.append(
                {
                    "inventory_id": index,
                    "product_id": (index % PRODUCT_COUNT) + 1,
                    "warehouse_id": (index % 5) + 1,
                    "stock_quantity": (index % 100) + 10,
                    "reorder_level": 5,
                }
            )

        write_csv(self.output_dir / "inventory.csv", rows)
        logger.info("Inventory generated: %s", len(rows))
        return rows
