"""Dataclass model for address entities."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


try:
    @dataclass(slots=True)
    class Address:
        """Represents a customer address in the e-commerce platform."""

        address_id: int
        address_line1: str
        address_line2: str
        city: str
        state: str
        country: str
        postal_code: str
        created_at: datetime
        updated_at: datetime
except TypeError:
    @dataclass
    class Address:
        """Represents a customer address in the e-commerce platform."""

        __slots__ = (
            "address_id",
            "address_line1",
            "address_line2",
            "city",
            "state",
            "country",
            "postal_code",
            "created_at",
            "updated_at",
        )

        address_id: int
        address_line1: str
        address_line2: str
        city: str
        state: str
        country: str
        postal_code: str
        created_at: datetime
        updated_at: datetime
