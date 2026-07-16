from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from ..logger import setup_logger
from ..models.brand import Brand
from ..services.catalog_service import CatalogService
from ..utils import ensure_output_dir, write_csv

logger = setup_logger(__name__)


class BrandGenerator:
    def __init__(self, output_dir: Path | str | None = None) -> None:
        self.output_dir = ensure_output_dir(output_dir)
        self._service = CatalogService()

    def generate(self, brands: List[Brand] | None = None, count: int = 0) -> List[Dict[str, Any]]:
        logger.info("Generating brands...")
        resolved_brands = brands if brands is not None else self._service.generate_brands(count=count or 24)
        rows = [self._to_row(brand) for brand in resolved_brands]
        write_csv(self.output_dir / "brands.csv", rows)
        logger.info("Brands generated: %s", len(rows))
        return rows

    def _to_row(self, brand: Brand) -> Dict[str, Any]:
        return {
            "brand_id": brand.brand_id,
            "brand_name": brand.brand_name,
        }
