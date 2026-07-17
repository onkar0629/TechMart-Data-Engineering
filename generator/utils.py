from __future__ import annotations

import random
import uuid
import csv
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd
from faker import Faker

from .config import OUTPUT_FOLDER
from .constants import EMAIL_DOMAINS

fake = Faker("en_IN")


def ensure_output_dir(output_dir: Path | str | None = None) -> Path:
    target = Path(output_dir or OUTPUT_FOLDER)
    target.mkdir(parents=True, exist_ok=True)
    return target


def write_csv(path: Path, rows: List[Dict[str, Any]]) -> None:
    if not rows:
        return

    path.parent.mkdir(parents=True, exist_ok=True)
    dataframe = pd.DataFrame(rows)
    dataframe.to_csv(path, index=False)


def read_csv_rows(path: Path) -> List[Dict[str, str]]:
    """Read a CSV file into dictionaries, returning an empty list when absent."""
    if not path.exists():
        return []

    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def generate_uuid() -> str:
    return str(uuid.uuid4())


def random_date(start_year: int, end_year: int | None = None) -> str:
    start = datetime(start_year, 1, 1)
    end = datetime(end_year or datetime.now().year, 12, 31)
    delta = end - start
    random_days = random.randint(0, delta.days)
    return (start + timedelta(days=random_days)).strftime("%Y-%m-%d")


def random_datetime(start_year: int, end_year: int | None = None) -> str:
    start = datetime(start_year, 1, 1)
    end = datetime(end_year or datetime.now().year, 12, 31)
    delta = end - start
    random_seconds = random.randint(0, int(delta.total_seconds()))
    return (start + timedelta(seconds=random_seconds)).strftime("%Y-%m-%d %H:%M:%S")


def generate_mobile_number() -> str:
    return f"9{random.randint(100000000, 999999999)}"


def create_email(first_name: str, last_name: str, used_emails: set[str] | None = None) -> str:
    clean_first = first_name.lower().replace(" ", "")
    clean_last = last_name.lower().replace(" ", "")
    domain = random.choices(
        population=list(EMAIL_DOMAINS.keys()),
        weights=list(EMAIL_DOMAINS.values()),
        k=1,
    )[0]
    email = f"{clean_first}.{clean_last}{random.randint(100, 999)}@{domain}"
    if used_emails is None:
        return email

    while email in used_emails:
        email = f"{clean_first}.{clean_last}{random.randint(100, 999)}@{domain}"
    return email


def create_phone_number(used_phones: set[str] | None = None) -> str:
    prefix = random.choice(["6", "7", "8", "9"])
    phone = f"{prefix}{random.randint(10000000, 99999999)}"
    if used_phones is None:
        return phone

    while phone in used_phones:
        phone = f"{prefix}{random.randint(10000000, 99999999)}"
    return phone


def random_date_between(start_date: date, end_date: date) -> date:
    if end_date < start_date:
        start_date, end_date = end_date, start_date
    delta_days = (end_date - start_date).days
    random_days = random.randint(0, delta_days)
    return start_date + timedelta(days=random_days)


def random_dob(min_age: int = 18, max_age: int = 70) -> date:
    today = date.today()
    min_birth = today - timedelta(days=max_age * 365)
    max_birth = today - timedelta(days=min_age * 365)
    return random_date_between(min_birth, max_birth)


def is_valid_age(date_of_birth: date, min_age: int = 18, max_age: int = 70) -> bool:
    age = (date.today() - date_of_birth).days // 365
    return min_age <= age <= max_age


def is_valid_registration_date(registration_date: date) -> bool:
    return registration_date <= date.today()


def safe_string(value: Any) -> str:
    return str(value) if value is not None else ""
