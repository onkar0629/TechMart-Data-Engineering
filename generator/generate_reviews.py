
from __future__ import annotations
from pathlib import Path
from typing import List, Dict, Any
from faker import Faker
from config import COUNTS
from utils import write_csv

fake = Faker("en_IN")

def generate_reviews(output_dir: Path) -> Path:
    rows: List[Dict[str, Any]] = []
    for index in range(1, COUNTS["reviews"] + 1):
        rows.append({
            "review_id": index,
            "customer_id": (index % COUNTS["customers"]) + 1,
            "product_id": (index % COUNTS["products"]) + 1,
            "rating": fake.random_int(min=1, max=5),
            "review_comment": fake.sentence(nb_words=10),
            "review_date": fake.date_time_between(start_date="-1y", end_date="now").strftime("%Y-%m-%d %H:%M:%S"),
            "is_verified": 1 if index % 3 == 0 else 0,
        })
    path = output_dir / "reviews.csv"
    write_csv(path, rows[0].keys(), rows)
    return path
