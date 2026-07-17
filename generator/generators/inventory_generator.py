from __future__ import annotations

import random
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List

from ..config import SEED
from ..constants import (
    MAX_CURRENT_STOCK,
    MIN_CURRENT_STOCK,
    MIN_REORDER_LEVEL,
    REORDER_LEVEL_RATIO,
    VALID_RETURN_STOCK_STATUSES,
)
from ..logger import setup_logger
from ..utils import ensure_output_dir, read_csv_rows, write_csv

logger = setup_logger(__name__)


class InventoryGenerator:
    """Generate inventory balances from product, sales, and return activity."""

    def __init__(self, output_dir: Path | str | None = None) -> None:
        self.output_dir = ensure_output_dir(output_dir)

    def generate(self) -> List[Dict[str, Any]]:
        """Write inventory rows where opening - sold + returned = current."""
        logger.info("Generating inventory...")
        rng = random.Random(SEED)
        product_ids = self._product_ids()
        units_sold_by_product = self._units_sold_by_product()
        units_returned_by_product = self._units_returned_by_product()
        rows: List[Dict[str, Any]] = []
        for index, product_id in enumerate(product_ids, start=1):
            units_sold = units_sold_by_product.get(product_id, 0)
            units_returned = min(units_returned_by_product.get(product_id, 0), units_sold)
            current_stock = rng.randint(MIN_CURRENT_STOCK, MAX_CURRENT_STOCK)
            opening_stock = current_stock + units_sold - units_returned
            rows.append(
                {
                    "inventory_id": index,
                    "product_id": product_id,
                    "warehouse_id": (index % 5) + 1,
                    "opening_stock": opening_stock,
                    "units_sold": units_sold,
                    "units_returned": units_returned,
                    "current_stock": current_stock,
                    "stock_quantity": current_stock,
                    "reorder_level": max(MIN_REORDER_LEVEL, int(current_stock * REORDER_LEVEL_RATIO)),
                }
            )

        write_csv(self.output_dir / "inventory.csv", rows)
        logger.info("Inventory generated: %s", len(rows))
        return rows

    def _product_ids(self) -> List[int]:
        products = self._read_csv("products.csv")
        if not products:
            return []
        return [int(row["product_id"]) for row in products if row.get("product_id")]

    def _units_sold_by_product(self) -> dict[int, int]:
        units_sold: dict[int, int] = defaultdict(int)
        for row in self._read_csv("order_items.csv"):
            if not row.get("product_id"):
                continue
            units_sold[int(row["product_id"])] += int(float(row.get("quantity") or 0))
        return units_sold

    def _units_returned_by_product(self) -> dict[int, int]:
        units_returned: dict[int, int] = defaultdict(int)
        for row in self._read_csv("returns.csv"):
            if not row.get("product_id"):
                continue
            if row.get("return_status") and row["return_status"] not in VALID_RETURN_STOCK_STATUSES:
                continue
            units_returned[int(row["product_id"])] += int(float(row.get("quantity") or 1))
        return units_returned

    def _read_csv(self, filename: str) -> List[Dict[str, str]]:
        path = self.output_dir / filename
        rows = read_csv_rows(path)
        if not rows:
            logger.warning("Skipping inventory source file because it does not exist: %s", filename)
        return rows
