
from __future__ import annotations
from pathlib import Path
from typing import List, Dict, Any
from faker import Faker
from config import COUNTS
from utils import write_csv

fake = Faker("en_IN")

def generate_returns(output_dir: Path) -> Path:
    rows: List[Dict[str, Any]] = []
    for index in range(1, COUNTS["returns"] + 1):
        rows.append({
            "return_id": index,
            "order_id": (index % COUNTS["orders"]) + 1,
            "product_id": (index % COUNTS["products"]) + 1,
            "return_reason": fake.random_element(elements=["Damaged", "Wrong Item", "Not as described", "Late delivery"]),
            "return_status": fake.random_element(elements=["Requested", "Approved", "Rejected", "Completed"]),
            "return_date": fake.date_time_between(start_date="-6m", end_date="now").strftime("%Y-%m-%d %H:%M:%S"),
            "refund_amount": round(50 + (index % 200), 2),
        })
    path = output_dir / "returns.csv"
    write_csv(path, rows[0].keys(), rows)
    return path
