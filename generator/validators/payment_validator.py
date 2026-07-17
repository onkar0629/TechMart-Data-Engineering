"""Payment data quality validation rules."""

from __future__ import annotations

from .base_validator import BaseValidator, ValidationResult


class PaymentValidator(BaseValidator):
    validator_name = "payment"

    def validate(self) -> ValidationResult:
        payments = self.read_csv("payments.csv")
        orders = {row["order_id"]: row for row in self.read_csv("orders.csv") if row.get("order_id")}
        duplicate_refs = self.duplicate_values(payments, "transaction_reference")

        for row in payments:
            payment_id = row.get("payment_id", "")
            order = orders.get(row.get("order_id", ""))
            self.check(order is not None, "order_fk", "Payment order_id does not exist", payment_id, "Order FK missing")
            self.check(
                order is not None
                and round(self.parse_float(row.get("payment_amount", row.get("amount", ""))), 2)
                == round(self.parse_float(order.get("total_amount", "")), 2),
                "amount_validation",
                "Payment amount does not match order total",
                payment_id,
                "Amount mismatch",
            )
            self.check(
                order is not None and row.get("payment_status", "") in self._allowed_payment_statuses(order.get("order_status", "")),
                "payment_status_consistency",
                "Payment status is inconsistent with order status",
                payment_id,
                "Invalid payment status",
            )
            self.check(
                row.get("transaction_reference", "") not in duplicate_refs,
                "transaction_reference_unique",
                "Duplicate transaction reference",
                payment_id,
                "Duplicate transaction reference",
            )

        return self.result

    def _allowed_payment_statuses(self, order_status: str) -> set[str]:
        if order_status in {"Delivered", "Shipped", "Packed"}:
            return {"Success"}
        if order_status == "Pending":
            return {"Pending"}
        if order_status == "Returned":
            return {"Refunded"}
        if order_status == "Cancelled":
            return {"Failed", "Refunded"}
        return set()
