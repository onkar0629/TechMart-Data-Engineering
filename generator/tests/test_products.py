"""Tests for product generator CSV row mapping."""

from __future__ import annotations

from pathlib import Path

from generator.generators.product_generator import ProductGenerator


def test_product_generator_writes_valid_product_rows(tmp_path: Path) -> None:
    rows = ProductGenerator(output_dir=tmp_path).generate(count=5)

    assert len(rows) == 5
    assert len({row["sku"] for row in rows}) == 5
    assert all(row["selling_price"] > row["cost_price"] for row in rows)
    assert (tmp_path / "products.csv").exists()
