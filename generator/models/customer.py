"""Dataclass model for customer entities."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime


try:
    @dataclass(slots=True)
    class Customer:
        """Represents a registered customer in the e-commerce platform."""

        customer_id: int
        first_name: str
        last_name: str
        email: str
        phone: str
        gender: str
        date_of_birth: date
        registration_date: date
        is_active: bool
        address_id: int
        created_at: datetime
        updated_at: datetime
except TypeError:
    @dataclass
    class Customer:
        """Represents a registered customer in the e-commerce platform."""

        __slots__ = (
            "customer_id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "gender",
            "date_of_birth",
            "registration_date",
            "is_active",
            "address_id",
            "created_at",
            "updated_at",
        )

        customer_id: int
        first_name: str
        last_name: str
        email: str
        phone: str
        gender: str
        date_of_birth: date
        registration_date: date
        is_active: bool
        address_id: int
        created_at: datetime
        updated_at: datetime
