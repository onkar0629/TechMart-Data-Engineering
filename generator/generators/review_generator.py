from __future__ import annotations

import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List

from ..config import REVIEW_COUNT, SEED
from ..constants import (
    MAX_DELIVERY_DAYS,
    MAX_REVIEW_DELAY_DAYS,
    MIN_DELIVERY_DAYS,
    MIN_REVIEW_DELAY_DAYS,
    REVIEW_COMMENTS,
    REVIEW_PROBABILITY,
    REVIEW_RATING_DISTRIBUTION,
    SECONDS_PER_DAY,
)
from ..logger import setup_logger
from ..utils import ensure_output_dir, read_csv_rows, write_csv

logger = setup_logger(__name__)


class ReviewGenerator:
    """Generate verified reviews from delivered customer purchases."""

    def __init__(self, output_dir: Path | str | None = None) -> None:
        self.output_dir = ensure_output_dir(output_dir)

    def generate(self) -> List[Dict[str, Any]]:
        """Write reviews for a realistic share of eligible delivered purchases."""
        logger.info("Generating reviews...")
        rng = random.Random(SEED)
        candidates = self._eligible_review_candidates()
        rng.shuffle(candidates)

        rows: List[Dict[str, Any]] = []
        for candidate in candidates:
            if len(rows) >= REVIEW_COUNT:
                break
            if rng.random() > REVIEW_PROBABILITY:
                continue

            review_id = len(rows) + 1
            delivery_date = candidate["order_date"] + timedelta(days=rng.randint(MIN_DELIVERY_DAYS, MAX_DELIVERY_DAYS))
            review_date = delivery_date + timedelta(
                days=rng.randint(MIN_REVIEW_DELAY_DAYS, MAX_REVIEW_DELAY_DAYS),
                seconds=rng.randint(0, SECONDS_PER_DAY),
            )
            rows.append(
                {
                    "review_id": review_id,
                    "customer_id": candidate["customer_id"],
                    "product_id": candidate["product_id"],
                    "rating": self._rating(rng),
                    "review_comment": rng.choice(REVIEW_COMMENTS),
                    "review_date": review_date.strftime("%Y-%m-%d %H:%M:%S"),
                    "is_verified": 1,
                }
            )

        write_csv(self.output_dir / "reviews.csv", rows)
        logger.info("Reviews generated: %s", len(rows))
        return rows

    def _eligible_review_candidates(self) -> List[Dict[str, Any]]:
        """Return the latest delivered purchase for each customer/product pair."""
        orders = {
            row["order_id"]: {
                "customer_id": row["customer_id"],
                "order_date": self._parse_datetime(row["order_date"]),
            }
            for row in self._read_csv("orders.csv")
            if row.get("order_id") and row.get("order_status") == "Delivered"
        }

        candidates_by_pair: dict[tuple[str, str], Dict[str, Any]] = {}
        for item in self._read_csv("order_items.csv"):
            order = orders.get(item.get("order_id", ""))
            if order is None:
                continue

            pair = (order["customer_id"], item.get("product_id", ""))
            existing_candidate = candidates_by_pair.get(pair)
            if existing_candidate is not None and existing_candidate["order_date"] >= order["order_date"]:
                continue

            candidates_by_pair[pair] = {
                "customer_id": order["customer_id"],
                "product_id": item["product_id"],
                "order_date": order["order_date"],
            }
        return list(candidates_by_pair.values())

    def _read_csv(self, filename: str) -> List[Dict[str, str]]:
        path = self.output_dir / filename
        rows = read_csv_rows(path)
        if not rows:
            logger.warning("Skipping review source file because it does not exist: %s", filename)
        return rows

    def _parse_datetime(self, value: str) -> datetime:
        for date_format in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
            try:
                return datetime.strptime(value, date_format)
            except ValueError:
                continue
        raise ValueError(f"Invalid order date for review generation: {value}")

    def _rating(self, rng: random.Random) -> int:
        return rng.choices(
            population=list(REVIEW_RATING_DISTRIBUTION.keys()),
            weights=list(REVIEW_RATING_DISTRIBUTION.values()),
            k=1,
        )[0]
