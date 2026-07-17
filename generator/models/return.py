"""Dataclass model for return entities."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Return:
    """Represents a customer return or refund workflow for an order item."""

    return_id: int
    order_id: int
    product_id: int
    return_reason: str
    return_status: str
    return_date: datetime
    refund_amount: float
