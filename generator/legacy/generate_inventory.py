
from __future__ import annotations
from pathlib import Path
from typing import List, Dict, Any
from config import COUNTS
from utils import write_csv

def generate_inventory(output_dir: Path) -> Path:
    rows: List[Dict[str, Any]] = []
    for index in range(1, COUNTS["inventory"] + 1):
        rows.append({
            "inventory_id": index,
            "product_id": (index % COUNTS["products"]) + 1,
            "warehouse_id": (index % 5) + 1,
            "stock_quantity": (index % 100) + 10,
            "reorder_level": 5,
            "last_updated_at": "2026-01-01 00:00:00",
        })
    path = output_dir / "inventory.csv"
    write_csv(path, rows[0].keys(), rows)
    return path
