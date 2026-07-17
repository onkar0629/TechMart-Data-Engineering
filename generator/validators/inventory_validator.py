"""Inventory data quality validation rules."""

from __future__ import annotations

from .base_validator import BaseValidator, ValidationResult


class InventoryValidator(BaseValidator):
    validator_name = "inventory"

    def validate(self) -> ValidationResult:
        inventory_rows = self.read_csv("inventory.csv")
        product_ids = self.ids_from_csv("products.csv", "product_id")

        for row in inventory_rows:
            inventory_id = row.get("inventory_id", "")
            self.check(
                self.parse_int(row.get("stock_quantity", "")) >= 0,
                "non_negative_stock",
                "Inventory stock_quantity must be non-negative",
                inventory_id,
                "Negative stock",
            )
            self.check(
                row.get("product_id", "") in product_ids,
                "product_fk",
                "Inventory product_id does not exist",
                inventory_id,
                "Product FK missing",
            )

        return self.result
