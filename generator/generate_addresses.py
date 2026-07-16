
from __future__ import annotations
from pathlib import Path
from typing import List, Dict, Any
from faker import Faker
from config import COUNTS
from utils import write_csv

fake = Faker("en_IN")

def generate_addresses(output_dir: Path) -> Path:
    rows: List[Dict[str, Any]] = []
    for index in range(1, COUNTS["addresses"] + 1):
        rows.append({
            "address_id": index,
            "address_line1": fake.street_address(),
            "address_line2": f"Unit {index % 50}" if index % 3 == 0 else "",
            "city": fake.city(),
            "state": fake.state(),
            "country": "India",
            "postal_code": fake.postcode(),
        })
    path = output_dir / "addresses.csv"
    write_csv(path, rows[0].keys(), rows)
    return path
