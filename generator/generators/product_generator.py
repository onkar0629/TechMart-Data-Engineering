from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from faker import Faker

from ..config import BRAND_COUNT, CATEGORY_COUNT, PRODUCT_COUNT, SUPPLIER_COUNT
from ..constants import CATEGORIES
from ..logger import setup_logger
from ..utils import ensure_output_dir, write_csv

logger = setup_logger(__name__)
fake = Faker("en_IN")


class ProductGenerator:
    def __init__(self, output_dir: Path | str | None = None) -> None:
        self.output_dir = ensure_output_dir(output_dir)

    def generate(self) -> List[Dict[str, Any]]:
        logger.info("Generating products...")
        rows: List[Dict[str, Any]] = []
        for index in range(1, PRODUCT_COUNT + 1):
            rows.append(
                {
                    "product_id": index,
                    "product_name": f"{fake.word().title()} {fake.word().title()}",
                    "brand_id": (index % BRAND_COUNT) + 1,
                    "category_id": (index % CATEGORY_COUNT) + 1,
                    "supplier_id": (index % SUPPLIER_COUNT) + 1,
                    "sku": f"SKU-{index:05d}",
                    "description": fake.sentence(nb_words=10),
                    "price": round(100 + float(index % 5000) + fake.random.uniform(0, 200), 2),
                    "cost_price": round(50 + float(index % 3000) + fake.random.uniform(0, 100), 2),
                    "is_available": True,
                }
            )

        write_csv(self.output_dir / "products.csv", rows)
        logger.info("Products generated: %s", len(rows))
        return rows
