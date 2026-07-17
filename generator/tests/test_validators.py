"""Tests for the reusable data quality validation framework."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from generator.validators.catalog_validator import CatalogValidator
from generator.validators.customer_validator import CustomerValidator
from generator.validators.order_validator import OrderValidator
from generator.validators.payment_validator import PaymentValidator
from generator.validators.review_validator import ReviewValidator
from generator.validators.validation_runner import ValidationRunner


def test_validation_runner_generates_reports_for_valid_dataset(tmp_path: Path) -> None:
    data_dir = tmp_path / "data"
    reports_dir = tmp_path / "reports"
    data_dir.mkdir()
    _write_valid_dataset(data_dir)

    results = ValidationRunner(data_dir=data_dir, reports_dir=reports_dir).run()

    assert all(result.overall_status == "Passed" for result in results)
    assert (reports_dir / "validation_report.json").exists()
    assert (reports_dir / "validation_report.csv").exists()
    assert (reports_dir / "validation_summary.md").exists()

    payload = json.loads((reports_dir / "validation_report.json").read_text(encoding="utf-8"))
    assert payload["summary"]["overall_status"] == "Passed"
    assert payload["summary"]["failed"] == 0
    assert payload["failure_breakdown"] == {}
    assert payload["sample_errors"] == []
    summary_markdown = (reports_dir / "validation_summary.md").read_text(encoding="utf-8")
    assert "Rows Checked" in summary_markdown
    assert "Failure Breakdown" in summary_markdown


def test_customer_validator_catches_duplicates_and_bad_fk(tmp_path: Path) -> None:
    _write_valid_dataset(tmp_path)
    _append_row(
        tmp_path / "customers.csv",
        {
            "customer_id": "3",
            "first_name": "Bad",
            "last_name": "Customer",
            "email": "a@example.com",
            "phone": "900000001",
            "gender": "Other",
            "date_of_birth": "2015-01-01",
            "registration_date": "2099-01-01",
            "status": "Active",
            "address_id": "999",
        },
    )

    result = CustomerValidator(tmp_path).validate()

    assert result.failed >= 5
    assert result.failure_categories["Duplicate email"] == 2
    assert result.failure_categories["Duplicate phone"] == 2
    assert result.failure_categories["Address FK missing"] == 1
    assert result.overall_status == "Failed"


def test_catalog_order_payment_and_review_validators_catch_rule_failures(tmp_path: Path) -> None:
    _write_valid_dataset(tmp_path)
    _replace_row(tmp_path / "products.csv", "product_id", "2", {"sku": "SKU-1", "brand_id": "999", "selling_price": "20"})
    _replace_row(tmp_path / "orders.csv", "order_id", "1", {"customer_id": "999", "total_amount": "1.00"})
    _append_row(
        tmp_path / "order_items.csv",
        {
            "order_item_id": "3",
            "order_id": "1",
            "product_id": "1",
            "quantity": "1",
            "unit_price": "50.00",
            "discount_percentage": "0",
        },
    )
    _replace_row(tmp_path / "payments.csv", "payment_id", "1", {"payment_status": "Pending", "payment_amount": "2.00"})
    _append_row(
        tmp_path / "payments.csv",
        {
            "payment_id": "3",
            "order_id": "2",
            "payment_method": "UPI",
            "payment_date": "2023-01-04 10:00:00",
            "payment_status": "Success",
            "payment_amount": "200.00",
            "transaction_reference": "TXN-2",
        },
    )
    _replace_row(tmp_path / "reviews.csv", "review_id", "1", {"product_id": "2", "rating": "6"})

    catalog_result = CatalogValidator(tmp_path).validate()
    order_result = OrderValidator(tmp_path).validate()
    payment_result = PaymentValidator(tmp_path).validate()
    review_result = ReviewValidator(tmp_path).validate()

    assert catalog_result.failed >= 3
    assert catalog_result.failure_categories["Duplicate SKU"] == 2
    assert catalog_result.failure_categories["Brand FK missing"] == 1
    assert catalog_result.failure_categories["Invalid selling price"] == 1

    assert order_result.failed >= 3
    assert order_result.failure_categories["Customer FK missing"] == 1
    assert order_result.failure_categories["Order total mismatch"] == 1
    assert order_result.failure_categories["Duplicate products"] == 1

    assert payment_result.failed >= 3
    assert payment_result.failure_categories["Amount mismatch"] == 1
    assert payment_result.failure_categories["Invalid payment status"] == 1
    assert payment_result.failure_categories["Duplicate transaction reference"] == 2

    assert review_result.failed >= 2
    assert review_result.failure_categories["Customer did not purchase product"] == 1
    assert review_result.failure_categories["Invalid rating"] == 1


def test_validation_report_includes_failure_breakdown_and_limited_samples(tmp_path: Path) -> None:
    data_dir = tmp_path / "data"
    reports_dir = tmp_path / "reports"
    data_dir.mkdir()
    _write_valid_dataset(data_dir)
    _replace_row(data_dir / "orders.csv", "order_id", "1", {"total_amount": "1.00"})
    _replace_row(data_dir / "payments.csv", "payment_id", "1", {"payment_status": "Pending", "payment_amount": "2.00"})

    ValidationRunner(data_dir=data_dir, reports_dir=reports_dir, max_reported_issues=2).run()

    payload = json.loads((reports_dir / "validation_report.json").read_text(encoding="utf-8"))
    assert "summary" in payload
    assert "failure_breakdown" in payload
    assert "sample_errors" in payload
    assert payload["failure_breakdown"]["order"]["Order total mismatch"] == 1
    assert payload["failure_breakdown"]["payment"]["Amount mismatch"] == 1
    assert payload["sample_errors_truncated"] is True
    assert len(payload["sample_errors"]) == 2
    assert "category" in payload["sample_errors"][0]

    summary_markdown = (reports_dir / "validation_summary.md").read_text(encoding="utf-8")
    assert "## Failure Breakdown" in summary_markdown
    assert "Order total mismatch: 1" in summary_markdown
    assert "Amount mismatch: 1" in summary_markdown


def _write_valid_dataset(path: Path) -> None:
    _write_csv(
        path / "addresses.csv",
        [
            {"address_id": "1", "address_line1": "A", "city": "Mumbai"},
            {"address_id": "2", "address_line1": "B", "city": "Pune"},
        ],
    )
    _write_csv(path / "brands.csv", [{"brand_id": "1", "brand_name": "Brand"}])
    _write_csv(path / "categories.csv", [{"category_id": "1", "category_name": "Category"}])
    _write_csv(path / "suppliers.csv", [{"supplier_id": "1", "supplier_name": "Supplier"}])
    _write_csv(
        path / "customers.csv",
        [
            {
                "customer_id": "1",
                "first_name": "A",
                "last_name": "One",
                "email": "a@example.com",
                "phone": "900000001",
                "gender": "Female",
                "date_of_birth": "1990-01-01",
                "registration_date": "2022-01-01",
                "status": "Active",
                "address_id": "1",
            },
            {
                "customer_id": "2",
                "first_name": "B",
                "last_name": "Two",
                "email": "b@example.com",
                "phone": "900000002",
                "gender": "Male",
                "date_of_birth": "1985-01-01",
                "registration_date": "2022-01-02",
                "status": "Active",
                "address_id": "2",
            },
        ],
    )
    _write_csv(
        path / "products.csv",
        [
            {
                "product_id": "1",
                "product_name": "Product 1",
                "brand_id": "1",
                "category_id": "1",
                "supplier_id": "1",
                "sku": "SKU-1",
                "cost_price": "50.00",
                "selling_price": "100.00",
            },
            {
                "product_id": "2",
                "product_name": "Product 2",
                "brand_id": "1",
                "category_id": "1",
                "supplier_id": "1",
                "sku": "SKU-2",
                "cost_price": "120.00",
                "selling_price": "200.00",
            },
        ],
    )
    _write_csv(
        path / "orders.csv",
        [
            {
                "order_id": "1",
                "customer_id": "1",
                "order_date": "2023-01-03 10:00:00",
                "order_status": "Delivered",
                "payment_status": "Success",
                "total_amount": "100.00",
                "shipping_address_id": "1",
            },
            {
                "order_id": "2",
                "customer_id": "2",
                "order_date": "2023-01-04 10:00:00",
                "order_status": "Shipped",
                "payment_status": "Success",
                "total_amount": "200.00",
                "shipping_address_id": "2",
            },
        ],
    )
    _write_csv(
        path / "order_items.csv",
        [
            {
                "order_item_id": "1",
                "order_id": "1",
                "product_id": "1",
                "quantity": "1",
                "unit_price": "100.00",
                "discount_percentage": "0",
            },
            {
                "order_item_id": "2",
                "order_id": "2",
                "product_id": "2",
                "quantity": "1",
                "unit_price": "200.00",
                "discount_percentage": "0",
            },
        ],
    )
    _write_csv(
        path / "payments.csv",
        [
            {
                "payment_id": "1",
                "order_id": "1",
                "payment_method": "UPI",
                "payment_date": "2023-01-03 10:01:00",
                "payment_status": "Success",
                "payment_amount": "100.00",
                "transaction_reference": "TXN-1",
            },
            {
                "payment_id": "2",
                "order_id": "2",
                "payment_method": "Credit Card",
                "payment_date": "2023-01-04 10:01:00",
                "payment_status": "Success",
                "payment_amount": "200.00",
                "transaction_reference": "TXN-2",
            },
        ],
    )
    _write_csv(
        path / "reviews.csv",
        [
            {
                "review_id": "1",
                "customer_id": "1",
                "product_id": "1",
                "rating": "5",
                "review_comment": "Great",
                "review_date": "2023-01-05",
            }
        ],
    )
    _write_csv(path / "inventory.csv", [{"inventory_id": "1", "product_id": "1", "stock_quantity": "10"}])


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _append_row(path: Path, row: dict[str, str]) -> None:
    rows = _read_csv(path)
    rows.append(row)
    _write_csv(path, rows)


def _replace_row(path: Path, key: str, value: str, updates: dict[str, str]) -> None:
    rows = _read_csv(path)
    for row in rows:
        if row[key] == value:
            row.update(updates)
    _write_csv(path, rows)


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))
