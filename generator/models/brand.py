"""Dataclass model for brand entities."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


try:
    @dataclass(slots=True)
    class Brand:
        """Represents a product brand in the catalog."""

        brand_id: int
        brand_name: str
        category_ids: tuple[int, ...]
        created_at: datetime
        updated_at: datetime
except TypeError:
    @dataclass
    class Brand:
        """Represents a product brand in the catalog."""

        __slots__ = ("brand_id", "brand_name", "category_ids", "created_at", "updated_at")

        brand_id: int
        brand_name: str
        category_ids: tuple[int, ...]
        created_at: datetime
        updated_at: datetime
