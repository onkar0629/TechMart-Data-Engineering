"""Dataclass model for supplier entities."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


try:
    @dataclass(slots=True)
    class Supplier:
        """Represents a supplier in the catalog."""

        supplier_id: int
        supplier_name: str
        contact_person: str
        email: str
        phone: str
        city: str
        state: str
        country: str
        rating: float
        created_at: datetime
        updated_at: datetime
except TypeError:
    @dataclass
    class Supplier:
        """Represents a supplier in the catalog."""

        __slots__ = ("supplier_id", "supplier_name", "contact_person", "email", "phone", "city", "state", "country", "rating", "created_at", "updated_at")

        supplier_id: int
        supplier_name: str
        contact_person: str
        email: str
        phone: str
        city: str
        state: str
        country: str
        rating: float
        created_at: datetime
        updated_at: datetime
