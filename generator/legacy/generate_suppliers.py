
from __future__ import annotations
from pathlib import Path
from typing import List, Dict, Any
from faker import Faker
from config import COUNTS
from utils import write_csv

fake = Faker("en_IN")

def generate_suppliers(output_dir: Path) -> Path:
    rows: List[Dict[str, Any]] = []
    for index in range(1, COUNTS["suppliers"] + 1):
        rows.append({
            "supplier_id": index,
            "supplier_name": fake.company(),
            "contact_person": fake.name(),
            "email": fake.email(),
            "phone": f"9{fake.random_number(digits=9, fix_len=True)}",
            "city": fake.city(),
            "state": fake.state(),
            "country": "India",
            "rating": round(fake.random.uniform(3.0, 5.0), 2),
        })
    path = output_dir / "suppliers.csv"
    write_csv(path, rows[0].keys(), rows)
    return path
