"""Dataclass model for inventory balance entities."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Inventory:
    """Represents stock movement and current inventory for one product."""

    inventory_id: int
    product_id: int
    warehouse_id: int
    opening_stock: int
    units_sold: int
    units_returned: int
    current_stock: int
    stock_quantity: int
    reorder_level: int
