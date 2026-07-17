"""Run all data quality validators and write validation reports."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Iterable, List

from ..config import OUTPUT_FOLDER, ROOT_DIR
from ..logger import setup_logger
from .base_validator import ValidationIssue, ValidationResult
from .catalog_validator import CatalogValidator
from .customer_validator import CustomerValidator
from .inventory_validator import InventoryValidator
from .order_validator import OrderValidator
from .payment_validator import PaymentValidator
from .review_validator import ReviewValidator

logger = setup_logger(__name__)

REPORTS_DIR = ROOT_DIR / "generator" / "reports"
MAX_REPORTED_ISSUES = 1000


class ValidationRunner:
    """Coordinate all data quality validators and report writers."""

    def __init__(
        self,
        data_dir: Path | str = OUTPUT_FOLDER,
        reports_dir: Path | str = REPORTS_DIR,
        max_reported_issues: int = MAX_REPORTED_ISSUES,
    ) -> None:
        self.data_dir = Path(data_dir)
        self.reports_dir = Path(reports_dir)
        self.max_reported_issues = max_reported_issues

    def run(self) -> List[ValidationResult]:
        logger.info("Starting data quality validation")
        validators = [
            CustomerValidator(self.data_dir),
            CatalogValidator(self.data_dir),
            OrderValidator(self.data_dir),
            PaymentValidator(self.data_dir),
            ReviewValidator(self.data_dir),
            InventoryValidator(self.data_dir),
        ]
        results: List[ValidationResult] = []

        for validator in validators:
            logger.info("Running %s validator", validator.validator_name)
            results.append(validator.validate())

        logger.info("Writing validation reports")
        self.write_reports(results)
        logger.info("Validation completed")
        return results

    def write_reports(self, results: Iterable[ValidationResult]) -> None:
        result_list = list(results)
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        self._write_json_report(result_list)
        self._write_csv_report(result_list)
        self._write_markdown_summary(result_list)

    def _write_json_report(self, results: List[ValidationResult]) -> None:
        payload = {
            "summary": self._summary(results),
            "failure_breakdown": self._failure_breakdown(results),
            "validators": [result.to_report_row() for result in results],
            "sample_errors_truncated": sum(len(result.errors) for result in results) > self.max_reported_issues,
            "sample_errors": [
                self._issue_to_dict(issue)
                for issue in [issue for result in results for issue in result.errors][: self.max_reported_issues]
            ],
        }
        with (self.reports_dir / "validation_report.json").open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2)

    def _write_csv_report(self, results: List[ValidationResult]) -> None:
        rows = [result.to_report_row() for result in results]
        with (self.reports_dir / "validation_report.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=[
                    "validator",
                    "rows_checked",
                    "passed",
                    "failed",
                    "warnings",
                    "errors",
                    "overall_status",
                ],
            )
            writer.writeheader()
            writer.writerows(rows)

    def _write_markdown_summary(self, results: List[ValidationResult]) -> None:
        summary = self._summary(results)
        lines = [
            "# Validation Summary",
            "",
            f"- Rows Checked: {summary['rows_checked']}",
            f"- Passed: {summary['passed']}",
            f"- Failed: {summary['failed']}",
            f"- Warnings: {summary['warnings']}",
            f"- Errors: {summary['errors']}",
            f"- Overall Status: {summary['overall_status']}",
            "",
            "| Validator | Rows Checked | Passed | Failed | Warnings | Errors | Overall Status |",
            "| --- | ---: | ---: | ---: | ---: | ---: | --- |",
        ]
        for result in results:
            row = result.to_report_row()
            lines.append(
                "| {validator} | {rows_checked} | {passed} | {failed} | {warnings} | {errors} | {overall_status} |".format(
                    **row
                )
            )

        lines.extend(["", "## Failure Breakdown", ""])
        breakdown = self._failure_breakdown(results)
        if not breakdown:
            lines.append("No validation failures detected.")
        else:
            for validator, failures in breakdown.items():
                lines.extend([f"### {validator.title()}", ""])
                for category, count in failures.items():
                    lines.append(f"- {category}: {count}")
                lines.append("")

        with (self.reports_dir / "validation_summary.md").open("w", encoding="utf-8") as handle:
            handle.write("\n".join(lines) + "\n")

    def _summary(self, results: List[ValidationResult]) -> dict[str, int | str]:
        failed = sum(result.failed for result in results)
        warnings = sum(result.warnings for result in results)
        errors = sum(1 for result in results for issue in result.errors if issue.severity == "error")
        return {
            "rows_checked": sum(result.rows_checked for result in results),
            "passed": sum(result.passed for result in results),
            "failed": failed,
            "warnings": warnings,
            "errors": errors,
            "overall_status": "Failed" if failed else "Passed with Warnings" if warnings else "Passed",
        }

    def _failure_breakdown(self, results: List[ValidationResult]) -> dict[str, dict[str, int]]:
        breakdown: dict[str, dict[str, int]] = {}
        for result in results:
            if not result.failure_categories:
                continue
            breakdown[result.validator] = dict(
                sorted(
                    result.failure_categories.items(),
                    key=lambda item: (-item[1], item[0]),
                )
            )
        return breakdown

    def _issue_to_dict(self, issue: ValidationIssue) -> dict[str, str]:
        return {
            "validator": issue.validator,
            "rule": issue.rule,
            "category": issue.category,
            "message": issue.message,
            "row_id": issue.row_id,
            "severity": issue.severity,
        }


def main() -> None:
    ValidationRunner().run()


if __name__ == "__main__":
    main()
