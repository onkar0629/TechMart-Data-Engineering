"""Dataclass model for review entities."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Review:
    """Represents a customer review for a purchased product."""

    review_id: int
    customer_id: int
    product_id: int
    rating: int
    review_comment: str
    review_date: datetime
    is_verified: bool
