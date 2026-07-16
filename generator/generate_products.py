
from __future__ import annotations
from pathlib import Path
from typing import List, Dict, Any
from faker import Faker
from config import COUNTS
from utils import write_csv

fake = Faker("en_IN")

def generate_products(output_dir: Path) -> Path:
    rows: List[Dict[str, Any]] = []
    for index in range(1, COUNTS["products"] + 1):
        rows.append({
            "product_id": index,
            "product_name": f"{fake.word().title()} {fake.word().title()}",
            "brand_id": (index % COUNTS["brands"]) + 1,
            "category_id": (index % COUNTS["categories"]) + 1,
            "supplier_id": (index % COUNTS["suppliers"]) + 1,
            "sku": f"SKU-{index:05d}",
            "description": fake.sentence(nb_words=8),
            "price": round(float(fake.random_number(digits=3)) + 100.0, 2),
            "cost_price": round(float(fake.random_number(digits=2)) + 50.0, 2),
            "is_active": 1,
        })
    path = output_dir / "products.csv"
    write_csv(path, rows[0].keys(), rows)
    return path
