
from __future__ import annotations
from pathlib import Path
from typing import List, Dict, Any
from faker import Faker
from config import COUNTS
from utils import write_csv

fake = Faker("en_IN")

def generate_orders(output_dir: Path) -> Path:
    rows: List[Dict[str, Any]] = []
    for index in range(1, COUNTS["orders"] + 1):
        rows.append({
            "order_id": index,
            "customer_id": (index % COUNTS["customers"]) + 1,
            "order_date": fake.date_time_between(start_date="-2y", end_date="now").strftime("%Y-%m-%d %H:%M:%S"),
            "order_status": fake.random_element(elements=["Pending", "Packed", "Shipped", "Delivered", "Cancelled", "Returned"]),
            "payment_status": fake.random_element(elements=["Pending", "Paid", "Failed", "Refunded"]),
            "total_amount": round(100 + (index % 5000), 2),
            "shipping_address_id": (index % COUNTS["addresses"]) + 1,
        })
    path = output_dir / "orders.csv"
    write_csv(path, rows[0].keys(), rows)
    return path
