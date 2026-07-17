"""Base classes and shared utilities for data quality validation."""

from __future__ import annotations

import csv
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List

from ..logger import setup_logger

logger = setup_logger(__name__)


@dataclass
class ValidationIssue:
    """Represents a single validation error or warning."""

    validator: str
    rule: str
    category: str
    message: str
    row_id: str = ""
    severity: str = "error"


@dataclass
class ValidationResult:
    """Aggregated result for one validator."""

    validator: str
    rows_checked: int = 0
    passed: int = 0
    failed: int = 0
    warnings: int = 0
    failure_categories: Dict[str, int] = field(default_factory=dict)
    errors: List[ValidationIssue] = field(default_factory=list)

    @property
    def overall_status(self) -> str:
        if self.failed:
            return "Failed"
        if self.warnings:
            return "Passed with Warnings"
        return "Passed"

    def to_report_row(self) -> Dict[str, Any]:
        return {
            "validator": self.validator,
            "rows_checked": self.rows_checked,
            "passed": self.passed,
            "failed": self.failed,
            "warnings": self.warnings,
            "errors": len([issue for issue in self.errors if issue.severity == "error"]),
            "overall_status": self.overall_status,
        }


class BaseValidator:
    """Common CSV loading, rule tracking, and conversion helpers."""

    validator_name = "base"

    def __init__(self, data_dir: Path | str) -> None:
        self.data_dir = Path(data_dir)
        self.result = ValidationResult(validator=self.validator_name)

    def validate(self) -> ValidationResult:
        raise NotImplementedError

    def read_csv(self, filename: str) -> List[Dict[str, str]]:
        path = self.data_dir / filename
        if not path.exists():
            self.add_error("file_exists", f"Missing required file: {filename}")
            return []

        with path.open(newline="", encoding="utf-8") as handle:
            return list(csv.DictReader(handle))

    def check(self, condition: bool, rule: str, message: str, row_id: str = "", category: str | None = None) -> None:
        self.result.rows_checked += 1
        if condition:
            self.result.passed += 1
            return

        self.result.failed += 1
        self.add_error(rule, message, row_id=row_id, category=category)

    def add_error(self, rule: str, message: str, row_id: str = "", category: str | None = None) -> None:
        failure_category = category or message
        self.result.failure_categories[failure_category] = self.result.failure_categories.get(failure_category, 0) + 1
        self.result.errors.append(
            ValidationIssue(
                validator=self.validator_name,
                rule=rule,
                category=failure_category,
                message=message,
                row_id=str(row_id),
                severity="error",
            )
        )

    def add_warning(self, rule: str, message: str, row_id: str = "", category: str | None = None) -> None:
        self.result.warnings += 1
        self.result.errors.append(
            ValidationIssue(
                validator=self.validator_name,
                rule=rule,
                category=category or message,
                message=message,
                row_id=str(row_id),
                severity="warning",
            )
        )

    def ids_from_csv(self, filename: str, id_column: str) -> set[str]:
        return {row[id_column] for row in self.read_csv(filename) if row.get(id_column)}

    def parse_float(self, value: str, default: float = 0.0) -> float:
        try:
            return float(value)
        except (TypeError, ValueError):
            return default

    def parse_int(self, value: str, default: int = 0) -> int:
        try:
            return int(float(value))
        except (TypeError, ValueError):
            return default

    def parse_datetime(self, value: str) -> datetime | None:
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
            try:
                return datetime.strptime(value, fmt)
            except (TypeError, ValueError):
                continue
        return None

    def age_on(self, birth_date: date, as_of: date) -> int:
        years = as_of.year - birth_date.year
        if (as_of.month, as_of.day) < (birth_date.month, birth_date.day):
            years -= 1
        return years

    def duplicate_values(self, rows: Iterable[Dict[str, str]], column: str) -> set[str]:
        seen: set[str] = set()
        duplicates: set[str] = set()
        for row in rows:
            value = row.get(column, "")
            if not value:
                continue
            if value in seen:
                duplicates.add(value)
            seen.add(value)
        return duplicates
