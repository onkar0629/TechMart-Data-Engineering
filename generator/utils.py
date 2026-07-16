from __future__ import annotations

import random
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd
from faker import Faker

from .config import OUTPUT_FOLDER

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


def safe_string(value: Any) -> str:
    return str(value) if value is not None else ""
