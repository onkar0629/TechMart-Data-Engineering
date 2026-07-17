"""Dataclass model for payment entities."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Payment:
    """Represents a payment attempt for an order."""

    payment_id: int
    order_id: int
    payment_method: str
    payment_date: datetime
    payment_status: str
    payment_amount: float
    transaction_reference: str
    created_at: datetime
