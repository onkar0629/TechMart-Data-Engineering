from __future__ import annotations

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
from .generators.shipment_generator import ShipmentGenerator
from .generators.supplier_generator import SupplierGenerator
from .logger import setup_logger

logger = setup_logger(__name__)


def main() -> None:
    start_time = time.time()
    output_dir = Path(OUTPUT_FOLDER)
    output_dir.mkdir(parents=True, exist_ok=True)

    generators = [
        ("addresses", AddressGenerator(output_dir)),
        ("brands", BrandGenerator(output_dir)),
        ("categories", CategoryGenerator(output_dir)),
        ("suppliers", SupplierGenerator(output_dir)),
        ("customers", CustomerGenerator(output_dir)),
        ("products", ProductGenerator(output_dir)),
        ("orders", OrderGenerator(output_dir)),
        ("order_items", OrderItemGenerator(output_dir)),
        ("payments", PaymentGenerator(output_dir)),
        ("reviews", ReviewGenerator(output_dir)),
        ("inventory", InventoryGenerator(output_dir)),
        ("shipments", ShipmentGenerator(output_dir)),
    ]

    for name, generator in generators:
        try:
            logger.info("Generating %s", name)
            generator.generate()
            logger.info("Completed %s", name)
        except Exception as exc:
            logger.exception("Failed to generate %s: %s", name, exc)

    elapsed = time.time() - start_time
    logger.info("Completed all generation tasks in %.2f seconds", elapsed)


if __name__ == "__main__":
    main()
