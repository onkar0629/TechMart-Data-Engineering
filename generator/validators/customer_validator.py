"""Customer data quality validation rules."""

from __future__ import annotations

from datetime import date

from .base_validator import BaseValidator, ValidationResult

MIN_CUSTOMER_AGE = 18
MAX_CUSTOMER_AGE = 70


class CustomerValidator(BaseValidator):
    validator_name = "customer"

    def validate(self) -> ValidationResult:
        customers = self.read_csv("customers.csv")
        address_ids = self.ids_from_csv("addresses.csv", "address_id")
        duplicate_emails = self.duplicate_values(customers, "email")
        duplicate_phones = self.duplicate_values(customers, "phone")
        today = date.today()

        for row in customers:
            row_id = row.get("customer_id", "")
            self.check(
                row.get("email", "") not in duplicate_emails,
                "unique_email",
                "Duplicate customer email",
                row_id,
                "Duplicate email",
            )
            self.check(
                row.get("phone", "") not in duplicate_phones,
                "unique_phone",
                "Duplicate customer phone",
                row_id,
                "Duplicate phone",
            )

            birth_datetime = self.parse_datetime(row.get("date_of_birth", ""))
            age = self.age_on(birth_datetime.date(), today) if birth_datetime else -1
            self.check(
                MIN_CUSTOMER_AGE <= age <= MAX_CUSTOMER_AGE,
                "age_range",
                f"Customer age outside {MIN_CUSTOMER_AGE}-{MAX_CUSTOMER_AGE}",
                row_id,
                "Invalid age",
            )

            registration_datetime = self.parse_datetime(row.get("registration_date", ""))
            self.check(
                registration_datetime is not None and registration_datetime.date() <= today,
                "registration_date",
                "Registration date is invalid or in the future",
                row_id,
                "Invalid registration date",
            )
            self.check(
                row.get("address_id", "") in address_ids,
                "address_fk",
                "Customer address_id does not exist",
                row_id,
                "Address FK missing",
            )

        return self.result
