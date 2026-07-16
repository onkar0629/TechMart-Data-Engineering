from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from ..logger import setup_logger
from ..models.supplier import Supplier
from ..services.catalog_service import CatalogService
from ..utils import ensure_output_dir, write_csv

logger = setup_logger(__name__)


class SupplierGenerator:
    def __init__(self, output_dir: Path | str | None = None) -> None:
        self.output_dir = ensure_output_dir(output_dir)
        self._service = CatalogService()

    def generate(self, suppliers: List[Supplier] | None = None, count: int = 0) -> List[Dict[str, Any]]:
        logger.info("Generating suppliers...")
        resolved_suppliers = suppliers if suppliers is not None else self._service.generate_suppliers(count=count or 100)
        rows = [self._to_row(supplier) for supplier in resolved_suppliers]
        write_csv(self.output_dir / "suppliers.csv", rows)
        logger.info("Suppliers generated: %s", len(rows))
        return rows

    def _to_row(self, supplier: Supplier) -> Dict[str, Any]:
        return {
            "supplier_id": supplier.supplier_id,
            "supplier_name": supplier.supplier_name,
            "contact_person": supplier.contact_person,
            "email": supplier.email,
            "phone": supplier.phone,
            "city": supplier.city,
            "state": supplier.state,
            "country": supplier.country,
            "rating": supplier.rating,
        }
