
from __future__ import annotations
from pathlib import Path
from typing import List, Dict, Any
from faker import Faker
from config import COUNTS
from utils import write_csv

fake = Faker("en_IN")

def generate_customers(output_dir: Path) -> Path:
    rows: List[Dict[str, Any]] = []
    for index in range(1, COUNTS["customers"] + 1):
        rows.append({
            "customer_id": index,
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.email(),
            "phone": f"9{fake.random_number(digits=9, fix_len=True)}",
            "gender": fake.random_element(elements=["Male", "Female", "Other", "Prefer not to say"]),
            "date_of_birth": fake.date_of_birth(minimum_age=18, maximum_age=70).strftime("%Y-%m-%d"),
            "registration_date": fake.date_between(start_date="-3y", end_date="today").strftime("%Y-%m-%d"),
            "status": fake.random_element(elements=["Active", "Inactive", "Suspended"]),
            "address_id": (index % COUNTS["addresses"]) + 1,
        })
    path = output_dir / "customers.csv"
    write_csv(path, rows[0].keys(), rows)
    return path
