"""Catalog data quality validation rules."""

from __future__ import annotations

from .base_validator import BaseValidator, ValidationResult


class CatalogValidator(BaseValidator):
    validator_name = "catalog"

    def validate(self) -> ValidationResult:
        products = self.read_csv("products.csv")
        brand_ids = self.ids_from_csv("brands.csv", "brand_id")
        category_ids = self.ids_from_csv("categories.csv", "category_id")
        supplier_ids = self.ids_from_csv("suppliers.csv", "supplier_id")
        duplicate_skus = self.duplicate_values(products, "sku")

        for row in products:
            row_id = row.get("product_id", "")
            self.check(row.get("sku", "") not in duplicate_skus, "unique_sku", "Duplicate product SKU", row_id, "Duplicate SKU")
            self.check(row.get("brand_id", "") in brand_ids, "brand_fk", "Product brand_id does not exist", row_id, "Brand FK missing")
            self.check(
                row.get("category_id", "") in category_ids,
                "category_fk",
                "Product category_id does not exist",
                row_id,
                "Category FK missing",
            )
            self.check(
                row.get("supplier_id", "") in supplier_ids,
                "supplier_fk",
                "Product supplier_id does not exist",
                row_id,
                "Supplier FK missing",
            )
            self.check(
                self.parse_float(row.get("selling_price", "")) > self.parse_float(row.get("cost_price", "")),
                "selling_price_gt_cost",
                "Product selling_price must be greater than cost_price",
                row_id,
                "Invalid selling price",
            )

        return self.result
