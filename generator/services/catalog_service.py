"""Business logic for generating validated product catalog entities."""

from __future__ import annotations

import random
from datetime import datetime
from typing import List

from faker import Faker

from ..config import BRAND_COUNT, CATEGORY_COUNT, PRODUCT_COUNT, SUPPLIER_COUNT
from ..constants import BRAND_NAMES, CATEGORIES
from ..logger import setup_logger
from ..models.brand import Brand
from ..models.category import Category
from ..models.product import Product
from ..models.supplier import Supplier
from ..utils import create_email, create_phone_number

logger = setup_logger(__name__)
fake = Faker("en_IN")


class CatalogService:
    """Generate realistic catalog objects with validated relationships."""

    def __init__(self) -> None:
        self._seen_skus: set[str] = set()
        self._seen_product_names: dict[int, set[str]] = {}

    def generate_categories(self, count: int = CATEGORY_COUNT) -> List[Category]:
        logger.info("Generating categories")
        categories: List[Category] = []
        for index, category_name in enumerate(CATEGORIES[:count], start=1):
            category = Category(
                category_id=index,
                category_name=category_name,
                min_price=self._category_price_range(category_name)[0],
                max_price=self._category_price_range(category_name)[1],
                markup_percentage=self._markup_percentage(category_name),
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
            categories.append(category)
        return categories

    def generate_brands(self, count: int = BRAND_COUNT) -> List[Brand]:
        logger.info("Generating brands")
        brands: List[Brand] = []
        for index, brand_name in enumerate(BRAND_NAMES[:count], start=1):
            brand = Brand(
                brand_id=index,
                brand_name=brand_name,
                category_ids=self._valid_category_ids(index),
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
            brands.append(brand)
        return brands

    def generate_suppliers(self, count: int = SUPPLIER_COUNT) -> List[Supplier]:
        logger.info("Generating suppliers")
        suppliers: List[Supplier] = []
        for index in range(1, count + 1):
            supplier = Supplier(
                supplier_id=index,
                supplier_name=fake.company(),
                contact_person=fake.name(),
                email=create_email(fake.first_name(), fake.last_name()),
                phone=create_phone_number(),
                city=fake.random_element(elements=["Mumbai", "Delhi", "Bengaluru", "Hyderabad", "Chennai", "Pune"]),
                state=fake.random_element(elements=["Maharashtra", "Delhi", "Karnataka", "Telangana", "Tamil Nadu"]),
                country="India",
                rating=round(fake.random.uniform(3.0, 5.0), 2),
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
            suppliers.append(supplier)
        return suppliers

    def generate_products(
        self,
        count: int = PRODUCT_COUNT,
        category_ids: List[int] | None = None,
        brand_ids: List[int] | None = None,
        supplier_ids: List[int] | None = None,
    ) -> List[Product]:
        logger.info("Generating products")
        categories = self.generate_categories(count=len(category_ids or [])) if category_ids else self.generate_categories()
        brands = self.generate_brands(count=len(brand_ids or [])) if brand_ids else self.generate_brands()
        suppliers = self.generate_suppliers(count=len(supplier_ids or [])) if supplier_ids else self.generate_suppliers()

        category_id_list = list(category_ids or [category.category_id for category in categories])
        brand_id_list = list(brand_ids or [brand.brand_id for brand in brands])
        supplier_id_list = list(supplier_ids or [supplier.supplier_id for supplier in suppliers])
        categories_by_id = {category.category_id: category for category in categories}
        brands_by_id = {brand.brand_id: brand for brand in brands}

        products: List[Product] = []
        for index in range(1, count + 1):
            category_id = category_id_list[(index - 1) % len(category_id_list)]
            brand_id = brand_id_list[(index - 1) % len(brand_id_list)]
            supplier_id = supplier_id_list[(index - 1) % len(supplier_id_list)]
            product = self._build_product(
                index=index,
                category_id=category_id,
                brand_id=brand_id,
                supplier_id=supplier_id,
                categories_by_id=categories_by_id,
                brands_by_id=brands_by_id,
            )
            if product is not None:
                products.append(product)
        return products

    def _build_product(
        self,
        index: int,
        category_id: int,
        brand_id: int,
        supplier_id: int,
        categories_by_id: dict[int, Category],
        brands_by_id: dict[int, Brand],
    ) -> Product | None:
        category = categories_by_id.get(category_id)
        brand = brands_by_id.get(brand_id)
        if category is None or brand is None:
            return None

        product_name = self._build_product_name(brand.brand_name, category.category_name)
        if self._is_duplicate_product_name(brand_id, product_name):
            return None

        cost_price = round(random.uniform(category.min_price, category.max_price), 2)
        selling_price = round(cost_price * (1 + category.markup_percentage / 100), 2)
        sku = self._build_sku(category.category_name, brand.brand_name, index)
        if sku in self._seen_skus:
            return None

        popularity = self._popularity_bucket(index)
        warranty_months = self._warranty_months(category.category_name)
        product = Product(
            product_id=index,
            product_name=product_name,
            brand_id=brand_id,
            category_id=category_id,
            supplier_id=supplier_id,
            sku=sku,
            description=f"{brand.brand_name} {category.category_name} built for reliable everyday use.",
            cost_price=cost_price,
            selling_price=selling_price,
            weight_grams=self._weight_grams(category.category_name),
            warranty_months=warranty_months,
            is_active=True,
            popularity=popularity,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        self._seen_skus.add(sku)
        self._seen_product_names.setdefault(brand_id, set()).add(product_name)
        return product

    def _build_product_name(self, brand_name: str, category_name: str) -> str:
        base_names = {
            "Electronics": ["Smart", "Lite", "Pro", "Ultra"],
            "Fashion": ["Classic", "Modern", "Urban", "Premium"],
            "Home Appliances": ["Comfort", "Fresh", "Glow", "Pure"],
            "Beauty": ["Glow", "Pure", "Radiant", "Soft"],
            "Books": ["Essential", "Insight", "Master", "Quick"],
        }
        prefix = random.choice(base_names.get(category_name, ["Essential", "Classic", "Pro", "Core"]))
        return f"{brand_name} {prefix} {category_name}"

    def _build_sku(self, category_name: str, brand_name: str, index: int) -> str:
        category_code = category_name[:3].upper()
        brand_code = brand_name[:3].upper()
        return f"{category_code}-{brand_code}-{index:06d}"

    def _category_price_range(self, category_name: str) -> tuple[float, float]:
        ranges = {
            "Electronics": (5000.0, 50000.0),
            "Fashion": (500.0, 10000.0),
            "Home Appliances": (1500.0, 40000.0),
            "Beauty": (200.0, 8000.0),
            "Books": (100.0, 5000.0),
            "Sports": (600.0, 12000.0),
            "Furniture": (2000.0, 60000.0),
            "Groceries": (50.0, 4000.0),
            "Toys": (300.0, 6000.0),
            "Health": (150.0, 7000.0),
            "Automotive": (1000.0, 20000.0),
            "Garden": (300.0, 8000.0),
            "Office": (400.0, 12000.0),
            "Jewelry": (1000.0, 50000.0),
            "Pet Supplies": (150.0, 6000.0),
            "Music": (400.0, 15000.0),
            "Movies": (100.0, 4000.0),
            "Gaming": (1000.0, 30000.0),
            "Travel": (500.0, 15000.0),
            "Food": (80.0, 4000.0),
        }
        return ranges.get(category_name, (200.0, 5000.0))

    def _markup_percentage(self, category_name: str) -> float:
        mapping = {
            "Electronics": 20.0,
            "Fashion": 35.0,
            "Home Appliances": 25.0,
            "Beauty": 30.0,
            "Books": 15.0,
            "Sports": 22.0,
            "Furniture": 28.0,
            "Groceries": 18.0,
            "Toys": 24.0,
            "Health": 20.0,
            "Automotive": 22.0,
            "Garden": 20.0,
            "Office": 18.0,
            "Jewelry": 30.0,
            "Pet Supplies": 20.0,
            "Music": 24.0,
            "Movies": 16.0,
            "Gaming": 25.0,
            "Travel": 22.0,
            "Food": 17.0,
        }
        return mapping.get(category_name, 20.0)

    def _valid_category_ids(self, brand_index: int) -> tuple[int, ...]:
        category_ids = list(range(1, min(CATEGORY_COUNT, 5) + 1))
        if brand_index % 2 == 0:
            category_ids = category_ids[:2]
        return tuple(category_ids)

    def _popularity_bucket(self, index: int) -> str:
        bucket = index % 10
        if bucket == 0:
            return "Fast Moving"
        if bucket in {1, 2, 3}:
            return "Medium"
        return "Slow Moving"

    def _warranty_months(self, category_name: str) -> int:
        mapping = {"Electronics": 12, "Home Appliances": 12, "Beauty": 6, "Furniture": 24, "Automotive": 12, "Gaming": 6}
        return mapping.get(category_name, 0)

    def _weight_grams(self, category_name: str) -> float:
        mapping = {
            "Electronics": 450.0,
            "Fashion": 220.0,
            "Home Appliances": 1800.0,
            "Beauty": 90.0,
            "Books": 350.0,
            "Sports": 800.0,
            "Furniture": 6000.0,
            "Groceries": 1000.0,
            "Toys": 300.0,
            "Health": 150.0,
            "Automotive": 2500.0,
            "Garden": 1200.0,
            "Office": 900.0,
            "Jewelry": 120.0,
            "Pet Supplies": 400.0,
            "Music": 500.0,
            "Movies": 250.0,
            "Gaming": 700.0,
            "Travel": 600.0,
            "Food": 250.0,
        }
        return mapping.get(category_name, 300.0)

    def _is_duplicate_product_name(self, brand_id: int, product_name: str) -> bool:
        names = self._seen_product_names.setdefault(brand_id, set())
        return product_name in names
