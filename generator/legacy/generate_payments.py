
from __future__ import annotations
from pathlib import Path
from typing import List, Dict, Any
from faker import Faker
from config import COUNTS
from utils import write_csv

fake = Faker("en_IN")

def generate_payments(output_dir: Path) -> Path:
    rows: List[Dict[str, Any]] = []
    for index in range(1, COUNTS["payments"] + 1):
        rows.append({
            "payment_id": index,
            "order_id": (index % COUNTS["orders"]) + 1,
            "payment_method": fake.random_element(elements=["UPI", "Credit Card", "Debit Card", "Wallet", "Net Banking", "Cash On Delivery"]),
            "payment_date": fake.date_time_between(start_date="-2y", end_date="now").strftime("%Y-%m-%d %H:%M:%S"),
            "payment_status": fake.random_element(elements=["Pending", "Success", "Failed", "Refunded"]),
            "amount": round(100 + (index % 5000), 2),
            "transaction_reference": f"TXN-{index:06d}",
            "gateway_response": fake.word(),
        })
    path = output_dir / "payments.csv"
    write_csv(path, rows[0].keys(), rows)
    return path
