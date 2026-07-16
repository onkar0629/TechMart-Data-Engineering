from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from faker import Faker

from ..config import ADDRESS_COUNT, CUSTOMER_COUNT, ORDER_COUNT, START_YEAR, END_YEAR
from ..constants import ORDER_STATUS_VALUES, PAYMENT_STATUS_VALUES
from ..logger import setup_logger
from ..utils import ensure_output_dir, random_datetime, write_csv

logger = setup_logger(__name__)
fake = Faker("en_IN")


class OrderGenerator:
    def __init__(self, output_dir: Path | str | None = None) -> None:
        self.output_dir = ensure_output_dir(output_dir)

    def generate(self) -> List[Dict[str, Any]]:
        logger.info("Generating orders...")
        rows: List[Dict[str, Any]] = []
        for index in range(1, ORDER_COUNT + 1):
            rows.append(
                {
                    "order_id": index,
                    "customer_id": (index % CUSTOMER_COUNT) + 1,
                    "order_date": random_datetime(START_YEAR, END_YEAR),
                    "order_status": fake.random_element(elements=ORDER_STATUS_VALUES),
                    "payment_status": fake.random_element(elements=PAYMENT_STATUS_VALUES),
                    "total_amount": round(100 + (index % 5000), 2),
                    "shipping_address_id": (index % ADDRESS_COUNT) + 1,
                    "billing_address_id": ((index + 1) % ADDRESS_COUNT) + 1,
                }
            )

        write_csv(self.output_dir / "orders.csv", rows)
        logger.info("Orders generated: %s", len(rows))
        return rows
