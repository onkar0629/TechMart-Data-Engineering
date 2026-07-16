from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from faker import Faker

from ..config import CUSTOMER_COUNT, PRODUCT_COUNT, REVIEW_COUNT
from ..constants import REVIEW_COMMENTS
from ..logger import setup_logger
from ..utils import ensure_output_dir, random_datetime, write_csv

logger = setup_logger(__name__)
fake = Faker("en_IN")


class ReviewGenerator:
    def __init__(self, output_dir: Path | str | None = None) -> None:
        self.output_dir = ensure_output_dir(output_dir)

    def generate(self) -> List[Dict[str, Any]]:
        logger.info("Generating reviews...")
        rows: List[Dict[str, Any]] = []
        for index in range(1, REVIEW_COUNT + 1):
            rows.append(
                {
                    "review_id": index,
                    "customer_id": (index % CUSTOMER_COUNT) + 1,
                    "product_id": (index % PRODUCT_COUNT) + 1,
                    "rating": fake.random_int(min=1, max=5),
                    "review_comment": fake.random_element(elements=REVIEW_COMMENTS),
                    "review_date": random_datetime(2021, 2026),
                    "is_verified": 1 if index % 3 == 0 else 0,
                }
            )

        write_csv(self.output_dir / "reviews.csv", rows)
        logger.info("Reviews generated: %s", len(rows))
        return rows
