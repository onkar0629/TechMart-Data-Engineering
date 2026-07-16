
from __future__ import annotations
from pathlib import Path
from typing import List, Dict, Any
from config import COUNTS
from utils import write_csv

def generate_order_items(output_dir: Path) -> Path:
    rows: List[Dict[str, Any]] = []
    for index in range(1, COUNTS["order_items"] + 1):
        rows.append({
            "order_item_id": index,
            "order_id": (index % COUNTS["orders"]) + 1,
            "product_id": (index % COUNTS["products"]) + 1,
            "quantity": (index % 5) + 1,
            "unit_price": round(100 + (index % 1000), 2),
            "discount": round((index % 10) * 0.5, 2),
        })
    path = output_dir / "order_items.csv"
    write_csv(path, rows[0].keys(), rows)
    return path
