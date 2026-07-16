from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from faker import Faker

from ..config import ADDRESS_COUNT
from ..constants import CITY_STATE_MAP, COUNTRIES
from ..logger import setup_logger
from ..models.address import Address
from ..utils import ensure_output_dir, write_csv

logger = setup_logger(__name__)
fake = Faker("en_IN")


class AddressGenerator:
    def __init__(self, output_dir: Path | str | None = None) -> None:
        self.output_dir = ensure_output_dir(output_dir)

    def generate(self, count: int = ADDRESS_COUNT) -> List[Address]:
        logger.info("Starting Address Generation")
        addresses: List[Address] = []
        for index in range(1, count + 1):
            city = fake.random_element(elements=list(CITY_STATE_MAP.keys()))
            state = CITY_STATE_MAP[city]
            address_line2 = f"Unit {index % 50}" if index % 3 == 0 else ""
            address = Address(
                address_id=index,
                address_line1=fake.street_address(),
                address_line2=address_line2,
                city=city,
                state=state,
                country=fake.random_element(elements=COUNTRIES),
                postal_code=fake.postcode(),
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
            addresses.append(address)

        rows = [self._to_row(address) for address in addresses]
        write_csv(self.output_dir / "addresses.csv", rows)
        logger.info("Addresses generated: %s", len(addresses))
        logger.info("CSV Written")
        return addresses

    def _to_row(self, address: Address) -> Dict[str, Any]:
        return {
            "address_id": address.address_id,
            "address_line1": address.address_line1,
            "address_line2": address.address_line2,
            "city": address.city,
            "state": address.state,
            "country": address.country,
            "postal_code": address.postal_code,
        }
