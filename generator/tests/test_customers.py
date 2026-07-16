"""Tests for the customer and address generation engine."""

from __future__ import annotations

import csv
from datetime import date, datetime
from pathlib import Path

from generator.generators.address_generator import AddressGenerator
from generator.generators.customer_generator import CustomerGenerator
from generator.services.customer_service import CustomerService


def test_customer_service_generates_unique_and_valid_customers(tmp_path: Path) -> None:
    address_generator = AddressGenerator(output_dir=tmp_path)
    address_generator.generate()

    service = CustomerService()
    customers = service.generate_customers(count=50, address_ids=[1, 2, 3, 4, 5])

    assert len(customers) == 50
    assert len({customer.email for customer in customers}) == 50
    assert len({customer.phone for customer in customers}) == 50

    for customer in customers:
        assert 18 <= (date.today() - customer.date_of_birth).days // 365 <= 70
        assert customer.registration_date <= date.today()
        assert customer.address_id in {1, 2, 3, 4, 5}
        assert isinstance(customer.created_at, datetime)
        assert isinstance(customer.updated_at, datetime)


def test_customer_generator_writes_expected_csv_rows(tmp_path: Path) -> None:
    address_generator = AddressGenerator(output_dir=tmp_path)
    address_generator.generate()

    customer_generator = CustomerGenerator(output_dir=tmp_path)
    rows = customer_generator.generate(count=25)

    assert len(rows) == 25

    with (tmp_path / "customers.csv").open(newline="", encoding="utf-8") as handle:
        loaded_rows = list(csv.DictReader(handle))

    assert len(loaded_rows) == 25
    assert "customer_id" in loaded_rows[0]
    assert "email" in loaded_rows[0]
    assert "phone" in loaded_rows[0]
