"""Dataclass model for order entities."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Order:
    """Represents a customer order."""

    order_id: int
    customer_id: int
    order_date: datetime
    order_status: str
    payment_status: str
    total_amount: float
    shipping_address_id: int
    billing_address_id: int
    created_at: datetime
