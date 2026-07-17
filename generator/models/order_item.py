"""Dataclass model for order item entities."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class OrderItem:
    """Represents a product purchased within an order."""

    order_item_id: int
    order_id: int
    product_id: int
    quantity: int
    unit_price: float
    discount_percentage: float
    created_at: datetime
