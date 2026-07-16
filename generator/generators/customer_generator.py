from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from faker import Faker

from ..config import ADDRESS_COUNT, CUSTOMER_COUNT, START_YEAR, END_YEAR
from ..constants import INDIAN_CITIES
from ..logger import setup_logger
from ..utils import ensure_output_dir, generate_mobile_number, random_date, write_csv

logger = setup_logger(__name__)
fake = Faker("en_IN")


class CustomerGenerator:
    def __init__(self, output_dir: Path | str | None = None) -> None:
        self.output_dir = ensure_output_dir(output_dir)

    def generate(self) -> List[Dict[str, Any]]:
        logger.info("Generating customers...")
        rows: List[Dict[str, Any]] = []
        for index in range(1, CUSTOMER_COUNT + 1):
            rows.append(
                {
                    "customer_id": index,
                    "first_name": fake.first_name(),
                    "last_name": fake.last_name(),
                    "email": fake.email(),
                    "phone": generate_mobile_number(),
                    "gender": fake.random_element(elements=["Male", "Female", "Other", "Prefer not to say"]),
                    "date_of_birth": fake.date_of_birth(minimum_age=18, maximum_age=70).strftime("%Y-%m-%d"),
                    "registration_date": random_date(START_YEAR, END_YEAR),
                    "status": fake.random_element(elements=["Active", "Inactive", "Suspended"]),
                    "address_id": (index % ADDRESS_COUNT) + 1,
                }
            )

        write_csv(self.output_dir / "customers.csv", rows)
        logger.info("Customers generated: %s", len(rows))
        return rows
