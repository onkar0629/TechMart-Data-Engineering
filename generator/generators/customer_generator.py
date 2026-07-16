from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from ..config import CUSTOMER_COUNT
from ..logger import setup_logger
from ..models.customer import Customer
from ..services.customer_service import CustomerService
from ..utils import ensure_output_dir, write_csv

logger = setup_logger(__name__)


class CustomerGenerator:
    def __init__(self, output_dir: Path | str | None = None) -> None:
        self.output_dir = ensure_output_dir(output_dir)
        self._service = CustomerService()

    def generate(self, customers: List[Customer] | None = None, count: int = CUSTOMER_COUNT, address_ids: List[int] | None = None) -> List[Dict[str, Any]]:
        logger.info("Starting Customer Generation")
        resolved_customers = customers if customers is not None else self._service.generate_customers(count=count, address_ids=address_ids)
        rows = [self._to_row(customer) for customer in resolved_customers]
        write_csv(self.output_dir / "customers.csv", rows)
        logger.info("Customers Generated: %s", len(rows))
        logger.info("CSV Written")
        return rows

    def _to_row(self, customer: Customer) -> Dict[str, Any]:
        return {
            "customer_id": customer.customer_id,
            "first_name": customer.first_name,
            "last_name": customer.last_name,
            "email": customer.email,
            "phone": customer.phone,
            "gender": customer.gender,
            "date_of_birth": customer.date_of_birth.strftime("%Y-%m-%d"),
            "registration_date": customer.registration_date.strftime("%Y-%m-%d"),
            "status": "Active" if customer.is_active else "Inactive",
            "address_id": customer.address_id,
        }
