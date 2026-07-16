from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from ..config import CATEGORY_COUNT
from ..constants import CATEGORIES
from ..logger import setup_logger
from ..utils import ensure_output_dir, write_csv

logger = setup_logger(__name__)


class CategoryGenerator:
    def __init__(self, output_dir: Path | str | None = None) -> None:
        self.output_dir = ensure_output_dir(output_dir)

    def generate(self) -> List[Dict[str, Any]]:
        logger.info("Generating categories...")
        rows: List[Dict[str, Any]] = []
        for index, category_name in enumerate(CATEGORIES[:CATEGORY_COUNT], start=1):
            rows.append(
                {
                    "category_id": index,
                    "category_name": category_name,
                }
            )

        write_csv(self.output_dir / "categories.csv", rows)
        logger.info("Categories generated: %s", len(rows))
        return rows
