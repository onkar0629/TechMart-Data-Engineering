
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
DATASETS_DIR = ROOT_DIR / "datasets"
RAW_DIR = DATASETS_DIR / "raw"
CLEANED_DIR = DATASETS_DIR / "cleaned"

COUNTS = {
    "addresses": 5000,
    "customers": 10000,
    "categories": 20,
    "brands": 100,
    "suppliers": 100,
    "products": 5000,
    "orders": 100000,
    "order_items": 300000,
    "payments": 100000,
    "reviews": 50000,
    "returns": 10000,
    "inventory": 5000,
}

MAX_ITEMS_PER_ORDER = 5
