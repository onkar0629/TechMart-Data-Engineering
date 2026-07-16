"""Dataclass model for category entities."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


try:
    @dataclass(slots=True)
    class Category:
        """Represents a product category in the catalog."""

        category_id: int
        category_name: str
        min_price: float
        max_price: float
        markup_percentage: float
        created_at: datetime
        updated_at: datetime
except TypeError:
    @dataclass
    class Category:
        """Represents a product category in the catalog."""

        __slots__ = ("category_id", "category_name", "min_price", "max_price", "markup_percentage", "created_at", "updated_at")

        category_id: int
        category_name: str
        min_price: float
        max_price: float
        markup_percentage: float
        created_at: datetime
        updated_at: datetime
