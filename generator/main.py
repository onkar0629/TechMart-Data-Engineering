from __future__ import annotations

import sys
import time
from pathlib import Path

from .config import OUTPUT_FOLDER
from .generators.address_generator import AddressGenerator
from .generators.brand_generator import BrandGenerator
from .generators.category_generator import CategoryGenerator
from .generators.customer_generator import CustomerGenerator
from .generators.inventory_generator import InventoryGenerator
from .generators.order_generator import OrderGenerator
from .generators.order_item_generator import OrderItemGenerator
from .generators.payment_generator import PaymentGenerator
from .generators.product_generator import ProductGenerator
from .generators.review_generator import ReviewGenerator
from .generators.supplier_generator import SupplierGenerator
from .logger import setup_logger
from .validators.validation_runner import ValidationRunner

logger = setup_logger(__name__)


def main() -> None:
    start_time = time.time()
    output_dir = Path(OUTPUT_FOLDER)
    output_dir.mkdir(parents=True, exist_ok=True)

    generators = [
        ("addresses", "Customer dependencies", AddressGenerator(output_dir)),
        ("categories", "Catalog dependencies", CategoryGenerator(output_dir)),
        ("brands", "Catalog dependencies", BrandGenerator(output_dir)),
        ("suppliers", "Catalog dependencies", SupplierGenerator(output_dir)),
        ("customers", "Generate Customers", CustomerGenerator(output_dir)),
        ("products", "Generate Catalog", ProductGenerator(output_dir)),
        ("orders", "Generate Orders", OrderGenerator(output_dir)),
        ("order_items", "Generate Orders", OrderItemGenerator(output_dir)),
        ("payments", "Generate Payments", PaymentGenerator(output_dir)),
        ("reviews", "Generate Reviews", ReviewGenerator(output_dir)),
        ("inventory", "Generate Inventory", InventoryGenerator(output_dir)),
    ]

    for name, stage, generator in generators:
        try:
            logger.info("%s: %s", stage, name)
            generator.generate()
            logger.info("Completed %s", name)
        except Exception as exc:
            logger.exception("Failed to generate %s: %s", name, exc)
            sys.exit(1)

    elapsed = time.time() - start_time
    logger.info("Completed all generation tasks in %.2f seconds", elapsed)

    logger.info("Running Validation Runner")
    validation_results = ValidationRunner(data_dir=output_dir).run()
    failed_results = [result for result in validation_results if result.failed]
    if failed_results:
        for result in failed_results:
            logger.error(
                "Validation failed for %s: rows_checked=%s passed=%s failed=%s warnings=%s errors=%s",
                result.validator,
                result.rows_checked,
                result.passed,
                result.failed,
                result.warnings,
                len([issue for issue in result.errors if issue.severity == "error"]),
            )
            for category, count in sorted(result.failure_categories.items(), key=lambda item: (-item[1], item[0])):
                logger.error("Validation failure summary [%s] %s: %s", result.validator, category, count)
        logger.error("Validation failed. Reports generated in generator/reports")
        sys.exit(1)

    logger.info("Validation passed. Reports generated in generator/reports")


if __name__ == "__main__":
    main()
