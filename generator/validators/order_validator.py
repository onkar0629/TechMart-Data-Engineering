"""Order data quality validation rules."""

from __future__ import annotations

from collections import defaultdict

from .base_validator import BaseValidator, ValidationResult


class OrderValidator(BaseValidator):
    validator_name = "order"

    def validate(self) -> ValidationResult:
        orders = self.read_csv("orders.csv")
        order_items = self.read_csv("order_items.csv")
        customer_ids = self.ids_from_csv("customers.csv", "customer_id")
        customer_registration = self._customer_registration_dates()
        items_by_order = defaultdict(list)

        for item in order_items:
            items_by_order[item.get("order_id", "")].append(item)

        for order in orders:
            order_id = order.get("order_id", "")
            self.check(
                order.get("customer_id", "") in customer_ids,
                "customer_fk",
                "Order customer_id does not exist",
                order_id,
                "Customer FK missing",
            )

            expected_total = round(
                sum(
                    round(
                        self.parse_int(item.get("quantity", ""))
                        * self.parse_float(item.get("unit_price", ""))
                        * (1 - self.parse_float(item.get("discount_percentage", item.get("discount", "0"))) / 100),
                        2,
                    )
                    for item in items_by_order.get(order_id, [])
                ),
                2,
            )
            self.check(
                round(self.parse_float(order.get("total_amount", "")), 2) == expected_total,
                "order_total",
                "Order total_amount does not match order item total",
                order_id,
                "Order total mismatch",
            )

            order_date = self.parse_datetime(order.get("order_date", ""))
            registration_date = customer_registration.get(order.get("customer_id", ""))
            self.check(
                order_date is not None and registration_date is not None and order_date >= registration_date,
                "order_date",
                "Order date is before customer registration date",
                order_id,
                "Invalid order date",
            )

            product_ids = [item.get("product_id", "") for item in items_by_order.get(order_id, [])]
            self.check(
                bool(product_ids) and len(product_ids) == len(set(product_ids)),
                "duplicate_products",
                "Order has duplicate products or no items",
                order_id,
                "Duplicate products",
            )

        return self.result

    def _customer_registration_dates(self):
        customers = self.read_csv("customers.csv")
        return {
            row["customer_id"]: self.parse_datetime(row.get("registration_date", ""))
            for row in customers
            if row.get("customer_id")
        }
