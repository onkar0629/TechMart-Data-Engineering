"""Business logic for generating validated customer entities."""

from __future__ import annotations

from datetime import date, datetime
from typing import List

from faker import Faker

from ..config import CUSTOMER_COUNT
from ..constants import GENDER_VALUES
from ..logger import setup_logger
from ..models.customer import Customer
from ..utils import create_email, create_phone_number, is_valid_age, is_valid_registration_date, random_date_between

logger = setup_logger(__name__)
fake = Faker("en_IN")


class CustomerService:
    """Generate realistic customer data with validation and uniqueness checks."""

    def __init__(self) -> None:
        self._seen_emails: set[str] = set()
        self._seen_phones: set[str] = set()

    def generate_customers(self, count: int = CUSTOMER_COUNT, address_ids: List[int] | None = None) -> List[Customer]:
        """Create validated customer objects for the requested count."""
        logger.info("Starting Customer Generation")
        customers: List[Customer] = []
        address_ids = list(address_ids or [1])
        validation_failures = 0

        for index in range(1, count + 1):
            customer = self._build_customer(index=index, address_ids=address_ids)
            if customer is None:
                validation_failures += 1
                continue
            customers.append(customer)

        logger.info("Customers Generated: %s", len(customers))
        logger.info("Validation Failures: %s", validation_failures)
        logger.info("Generation Completed")
        return customers

    def _build_customer(self, index: int, address_ids: List[int]) -> Customer | None:
        for _ in range(1000):
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = create_email(first_name, last_name, self._seen_emails)
            phone = create_phone_number(self._seen_phones)
            date_of_birth = self._random_dob(min_age=18, max_age=70)
            registration_date = random_date_between(datetime(2021, 1, 1).date(), datetime.now().date())
            address_id = address_ids[(index - 1) % len(address_ids)]
            is_active = fake.random.random() < 0.8

            if not self._is_valid(
                email=email,
                phone=phone,
                date_of_birth=date_of_birth,
                registration_date=registration_date,
                address_id=address_id,
            ):
                logger.debug("Validation failed for customer %s", index)
                continue

            customer = Customer(
                customer_id=index,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                gender=fake.random_element(elements=GENDER_VALUES),
                date_of_birth=date_of_birth,
                registration_date=registration_date,
                is_active=is_active,
                address_id=address_id,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
            self._seen_emails.add(email)
            self._seen_phones.add(phone)
            return customer

        return None

    def _is_valid(self, *, email: str, phone: str, date_of_birth: date, registration_date: date, address_id: int) -> bool:
        if email in self._seen_emails:
            return False
        if phone in self._seen_phones:
            return False
        if not is_valid_age(date_of_birth):
            return False
        if not is_valid_registration_date(registration_date):
            return False
        return address_id > 0

    def _random_dob(self, min_age: int, max_age: int) -> date:
        today = date.today()
        earliest_birth_date = self._years_before(today, max_age)
        latest_birth_date = self._years_before(today, min_age)
        return random_date_between(earliest_birth_date, latest_birth_date)

    def _years_before(self, value: date, years: int) -> date:
        try:
            return value.replace(year=value.year - years)
        except ValueError:
            return value.replace(year=value.year - years, day=28)
