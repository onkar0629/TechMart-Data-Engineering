from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from faker import Faker

from ..config import ADDRESS_COUNT
from ..constants import INDIAN_CITIES, INDIAN_STATES, COUNTRIES
from ..logger import setup_logger
from ..utils import ensure_output_dir, write_csv

logger = setup_logger(__name__)
fake = Faker("en_IN")


class AddressGenerator:
    def __init__(self, output_dir: Path | str | None = None) -> None:
        self.output_dir = ensure_output_dir(output_dir)

    def generate(self) -> List[Dict[str, Any]]:
        logger.info("Generating addresses...")
        rows: List[Dict[str, Any]] = []
        for index in range(1, ADDRESS_COUNT + 1):
            rows.append(
                {
                    "address_id": index,
                    "address_line1": fake.street_address(),
                    "address_line2": f"Unit {index % 50}" if index % 3 == 0 else "",
                    "city": fake.random_element(elements=INDIAN_CITIES),
                    "state": fake.random_element(elements=INDIAN_STATES),
                    "country": fake.random_element(elements=COUNTRIES),
                    "postal_code": fake.postcode(),
                }
            )

        write_csv(self.output_dir / "addresses.csv", rows)
        logger.info("Addresses generated: %s", len(rows))
        return rows
