from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from ..config import BRAND_COUNT
from ..constants import BRAND_NAMES
from ..logger import setup_logger
from ..utils import ensure_output_dir, write_csv

logger = setup_logger(__name__)


class BrandGenerator:
    def __init__(self, output_dir: Path | str | None = None) -> None:
        self.output_dir = ensure_output_dir(output_dir)

    def generate(self) -> List[Dict[str, Any]]:
        logger.info("Generating brands...")
        rows: List[Dict[str, Any]] = []
        for index, brand_name in enumerate(BRAND_NAMES[:BRAND_COUNT], start=1):
            rows.append(
                {
                    "brand_id": index,
                    "brand_name": brand_name,
                }
            )

        write_csv(self.output_dir / "brands.csv", rows)
        logger.info("Brands generated: %s", len(rows))
        return rows
