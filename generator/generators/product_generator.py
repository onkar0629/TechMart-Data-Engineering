from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from ..logger import setup_logger
from ..models.product import Product
from ..services.catalog_service import CatalogService
from ..utils import ensure_output_dir, write_csv

logger = setup_logger(__name__)


class ProductGenerator:
    def __init__(self, output_dir: Path | str | None = None) -> None:
        self.output_dir = ensure_output_dir(output_dir)
        self._service = CatalogService()

    def generate(
        self,
        products: List[Product] | None = None,
        count: int = 0,
        category_ids: List[int] | None = None,
        brand_ids: List[int] | None = None,
        supplier_ids: List[int] | None = None,
    ) -> List[Dict[str, Any]]:
        logger.info("Generating products...")
        resolved_products = products if products is not None else self._service.generate_products(
            count=count or 5000,
            category_ids=category_ids,
            brand_ids=brand_ids,
            supplier_ids=supplier_ids,
        )
        rows = [self._to_row(product) for product in resolved_products]
        write_csv(self.output_dir / "products.csv", rows)
        logger.info("Products generated: %s", len(rows))
        return rows

    def _to_row(self, product: Product) -> Dict[str, Any]:
        return {
            "product_id": product.product_id,
            "product_name": product.product_name,
            "brand_id": product.brand_id,
            "category_id": product.category_id,
            "supplier_id": product.supplier_id,
            "sku": product.sku,
            "description": product.description,
            "cost_price": product.cost_price,
            "selling_price": product.selling_price,
            "weight_grams": product.weight_grams,
            "warranty_months": product.warranty_months,
            "is_active": product.is_active,
            "popularity": product.popularity,
        }
