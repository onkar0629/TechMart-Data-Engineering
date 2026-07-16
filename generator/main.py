
from config import RAW_DIR, CLEANED_DIR
from generate_addresses import generate_addresses
from generate_categories import generate_categories
from generate_customers import generate_customers
from generate_suppliers import generate_suppliers
from generate_products import generate_products
from generate_orders import generate_orders
from generate_order_items import generate_order_items
from generate_payments import generate_payments
from generate_reviews import generate_reviews
from generate_returns import generate_returns
from generate_inventory import generate_inventory

def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    CLEANED_DIR.mkdir(parents=True, exist_ok=True)

    print("Starting TechMart data generation...")
    generate_addresses(RAW_DIR)
    generate_categories(RAW_DIR)
    generate_customers(RAW_DIR)
    generate_suppliers(RAW_DIR)
    generate_products(RAW_DIR)
    generate_orders(RAW_DIR)
    generate_order_items(RAW_DIR)
    generate_payments(RAW_DIR)
    generate_reviews(RAW_DIR)
    generate_returns(RAW_DIR)
    generate_inventory(RAW_DIR)
    print("Data generation completed.")

if __name__ == "__main__":
    main()
