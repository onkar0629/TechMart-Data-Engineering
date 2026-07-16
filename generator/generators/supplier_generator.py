from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from faker import Faker

from ..config import SUPPLIER_COUNT
from ..constants import COUNTRIES, INDIAN_CITIES, INDIAN_STATES
from ..logger import setup_logger
from ..utils import ensure_output_dir, generate_mobile_number, write_csv

logger = setup_logger(__name__)
fake = Faker("en_IN")


class SupplierGenerator:
    def __init__(self, output_dir: Path | str | None = None) -> None:
        self.output_dir = ensure_output_dir(output_dir)

    def generate(self) -> List[Dict[str, Any]]:
        logger.info("Generating suppliers...")
        rows: List[Dict[str, Any]] = []
        for index in range(1, SUPPLIER_COUNT + 1):
            rows.append(
                {
                    "supplier_id": index,
                    "supplier_name": fake.company(),
                    "contact_person": fake.name(),
                    "email": fake.email(),
                    "phone": generate_mobile_number(),
                    "city": fake.random_element(elements=INDIAN_CITIES),
                    "state": fake.random_element(elements=INDIAN_STATES),
                    "country": fake.random_element(elements=COUNTRIES),
                    "rating": round(fake.random.uniform(3.0, 5.0), 2),
                }
            )

        write_csv(self.output_dir / "suppliers.csv", rows)
        logger.info("Suppliers generated: %s", len(rows))
        return rows
