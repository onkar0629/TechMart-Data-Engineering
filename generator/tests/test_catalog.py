"""Tests for the product catalog engine."""

from __future__ import annotations

from generator.services.catalog_service import CatalogService


def test_catalog_service_generates_valid_products() -> None:
    service = CatalogService()
    categories = service.generate_categories(count=5)
    brands = service.generate_brands(count=6)
    suppliers = service.generate_suppliers(count=4)
    products = service.generate_products(
        count=12,
        category_ids=[category.category_id for category in categories],
        brand_ids=[brand.brand_id for brand in brands],
        supplier_ids=[supplier.supplier_id for supplier in suppliers],
    )

    assert len(products) == 12
    assert len({product.sku for product in products}) == 12

    for product in products:
        assert product.selling_price > product.cost_price
        assert product.brand_id in {brand.brand_id for brand in brands}
        assert product.category_id in {category.category_id for category in categories}
        assert product.supplier_id in {supplier.supplier_id for supplier in suppliers}

    seen_names: dict[int, set[str]] = {}
    for product in products:
        seen_names.setdefault(product.brand_id, set()).add(product.product_name)

    for names in seen_names.values():
        assert len(names) == len(list(names))
