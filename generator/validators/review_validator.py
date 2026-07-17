"""Review data quality validation rules."""

from __future__ import annotations

from .base_validator import BaseValidator, ValidationResult


class ReviewValidator(BaseValidator):
    validator_name = "review"

    def validate(self) -> ValidationResult:
        reviews = self.read_csv("reviews.csv")
        purchased_pairs = self._purchased_customer_products()

        for row in reviews:
            review_id = row.get("review_id", "")
            customer_product = (row.get("customer_id", ""), row.get("product_id", ""))
            self.check(
                customer_product in purchased_pairs,
                "customer_purchased_product",
                "Review customer did not purchase reviewed product",
                review_id,
                "Customer did not purchase product",
            )
            rating = self.parse_int(row.get("rating", ""))
            self.check(1 <= rating <= 5, "rating_range", "Review rating must be between 1 and 5", review_id, "Invalid rating")

        return self.result

    def _purchased_customer_products(self) -> set[tuple[str, str]]:
        orders = {row["order_id"]: row["customer_id"] for row in self.read_csv("orders.csv") if row.get("order_id")}
        pairs: set[tuple[str, str]] = set()
        for item in self.read_csv("order_items.csv"):
            customer_id = orders.get(item.get("order_id", ""))
            if customer_id:
                pairs.add((customer_id, item.get("product_id", "")))
        return pairs
