from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from ..logger import setup_logger
from ..models.category import Category
from ..services.catalog_service import CatalogService
from ..utils import ensure_output_dir, write_csv

logger = setup_logger(__name__)


class CategoryGenerator:
    def __init__(self, output_dir: Path | str | None = None) -> None:
        self.output_dir = ensure_output_dir(output_dir)
        self._service = CatalogService()

    def generate(self, categories: List[Category] | None = None, count: int = 0) -> List[Dict[str, Any]]:
        logger.info("Generating categories...")
        resolved_categories = categories if categories is not None else self._service.generate_categories(count=count or 20)
        rows = [self._to_row(category) for category in resolved_categories]
        write_csv(self.output_dir / "categories.csv", rows)
        logger.info("Categories generated: %s", len(rows))
        return rows

    def _to_row(self, category: Category) -> Dict[str, Any]:
        return {
            "category_id": category.category_id,
            "category_name": category.category_name,
        }
