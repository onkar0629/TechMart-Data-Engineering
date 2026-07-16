from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from faker import Faker

from ..config import ORDER_COUNT, PAYMENT_COUNT
from ..constants import PAYMENT_METHODS, PAYMENT_STATUS_VALUES
from ..logger import setup_logger
from ..utils import ensure_output_dir, random_datetime, write_csv

logger = setup_logger(__name__)
fake = Faker("en_IN")


class PaymentGenerator:
    def __init__(self, output_dir: Path | str | None = None) -> None:
        self.output_dir = ensure_output_dir(output_dir)

    def generate(self) -> List[Dict[str, Any]]:
        logger.info("Generating payments...")
        rows: List[Dict[str, Any]] = []
        for index in range(1, PAYMENT_COUNT + 1):
            rows.append(
                {
                    "payment_id": index,
                    "order_id": (index % ORDER_COUNT) + 1,
                    "payment_method": fake.random_element(elements=PAYMENT_METHODS),
                    "payment_date": random_datetime(2021, 2026),
                    "payment_status": fake.random_element(elements=PAYMENT_STATUS_VALUES),
                    "payment_amount": round(100 + (index % 5000), 2),
                    "transaction_reference": f"TXN-{index:06d}",
                }
            )

        write_csv(self.output_dir / "payments.csv", rows)
        logger.info("Payments generated: %s", len(rows))
        return rows
