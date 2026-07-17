"""Inventory service extension point.

Inventory balances are currently calculated inside the inventory generator from
product, order item, and optional return CSV inputs. This module remains as a
documented architectural slot for future inventory-specific business rules.
"""

from __future__ import annotations


class InventoryService:
    """Reserved service boundary for future inventory workflows."""
