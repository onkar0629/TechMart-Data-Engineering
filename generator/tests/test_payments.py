"""Tests for payment model and generator surfaces."""

from __future__ import annotations

from datetime import datetime

from generator.models.payment import Payment


def test_payment_model_captures_transaction_fields() -> None:
    payment = Payment(
        payment_id=1,
        order_id=10,
        payment_method="UPI",
        payment_date=datetime(2024, 1, 1, 10, 0, 0),
        payment_status="Success",
        payment_amount=999.99,
        transaction_reference="TXN-000000000010-example",
        created_at=datetime(2024, 1, 1, 10, 0, 0),
    )

    assert payment.order_id == 10
    assert payment.payment_amount == 999.99
    assert payment.transaction_reference.startswith("TXN-")
