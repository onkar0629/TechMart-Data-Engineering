from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from faker import Faker

from ..config import ORDER_COUNT
from ..constants import SHIPMENT_STATUS_VALUES
from ..logger import setup_logger
from ..utils import ensure_output_dir, write_csv

logger = setup_logger(__name__)
fake = Faker("en_IN")


class ShipmentGenerator:
    def __init__(self, output_dir: Path | str | None = None) -> None:
        self.output_dir = ensure_output_dir(output_dir)

    def generate(self) -> List[Dict[str, Any]]:
        logger.info("Generating shipments...")
        rows: List[Dict[str, Any]] = []
        for index in range(1, ORDER_COUNT + 1):
            rows.append(
                {
                    "shipment_id": index,
                    "order_id": index,
                    "warehouse_id": (index % 5) + 1,
                    "tracking_number": f"TRK{index:06d}",
                    "shipment_status": fake.random_element(elements=SHIPMENT_STATUS_VALUES),
                }
            )

        write_csv(self.output_dir / "shipments.csv", rows)
        logger.info("Shipments generated: %s", len(rows))
        return rows
