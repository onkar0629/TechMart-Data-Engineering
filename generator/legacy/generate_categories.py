
from __future__ import annotations
from pathlib import Path
from typing import List, Dict, Any
from config import COUNTS
from utils import write_csv

def generate_categories(output_dir: Path) -> Path:
    base_categories = [
        "Electronics", "Home Appliances", "Fashion", "Beauty", "Books", "Sports", "Furniture", "Groceries",
        "Toys", "Health", "Automotive", "Garden", "Office", "Jewelry", "Pet Supplies", "Music", "Movies",
        "Gaming", "Travel", "Food"
    ]
    rows: List[Dict[str, Any]] = []
    for index, category_name in enumerate(base_categories[:COUNTS["categories"]], start=1):
        rows.append({
            "category_id": index,
            "category_name": category_name,
            "parent_category_id": "",
            "description": f"{category_name} category",
        })
    path = output_dir / "categories.csv"
    write_csv(path, rows[0].keys(), rows)
    return path
