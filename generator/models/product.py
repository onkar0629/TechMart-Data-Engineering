"""Dataclass model for product entities."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


try:
    @dataclass(slots=True)
    class Product:
        """Represents a product in the catalog."""

        product_id: int
        product_name: str
        brand_id: int
        category_id: int
        supplier_id: int
        sku: str
        description: str
        cost_price: float
        selling_price: float
        weight_grams: float
        warranty_months: int
        is_active: bool
        popularity: str
        created_at: datetime
        updated_at: datetime
except TypeError:
    @dataclass
    class Product:
        """Represents a product in the catalog."""

        __slots__ = (
            "product_id",
            "product_name",
            "brand_id",
            "category_id",
            "supplier_id",
            "sku",
            "description",
            "cost_price",
            "selling_price",
            "weight_grams",
            "warranty_months",
            "is_active",
            "popularity",
            "created_at",
            "updated_at",
        )

        product_id: int
        product_name: str
        brand_id: int
        category_id: int
        supplier_id: int
        sku: str
        description: str
        cost_price: float
        selling_price: float
        weight_grams: float
        warranty_months: int
        is_active: bool
        popularity: str
        created_at: datetime
        updated_at: datetime
