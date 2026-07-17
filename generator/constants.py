from __future__ import annotations

CITY_STATE_MAP = {
    "Mumbai": "Maharashtra",
    "Delhi": "Delhi",
    "Bengaluru": "Karnataka",
    "Hyderabad": "Telangana",
    "Chennai": "Tamil Nadu",
    "Kolkata": "West Bengal",
    "Pune": "Maharashtra",
    "Jaipur": "Rajasthan",
    "Ahmedabad": "Gujarat",
    "Lucknow": "Uttar Pradesh",
    "Kanpur": "Uttar Pradesh",
    "Nagpur": "Maharashtra",
    "Visakhapatnam": "Andhra Pradesh",
    "Surat": "Gujarat",
    "Coimbatore": "Tamil Nadu",
    "Indore": "Madhya Pradesh",
    "Vadodara": "Gujarat",
    "Bhopal": "Madhya Pradesh",
    "Thane": "Maharashtra",
    "Agra": "Uttar Pradesh",
}

INDIAN_CITIES = list(CITY_STATE_MAP.keys())
INDIAN_STATES = list(dict.fromkeys(CITY_STATE_MAP.values()))

COUNTRIES = ["India"]

EMAIL_DOMAINS = {
    "gmail.com": 0.70,
    "outlook.com": 0.15,
    "yahoo.com": 0.10,
    "icloud.com": 0.05,
}

GENDER_VALUES = ["Male", "Female", "Other", "Prefer not to say"]
CUSTOMER_STATUS_VALUES = ["Active", "Inactive", "Suspended"]
SHIPMENT_STATUS_VALUES = ["Pending", "Packed", "In Transit", "Delivered", "Failed"]
RETURN_STATUS_VALUES = ["Requested", "Approved", "Rejected", "Completed"]

CATEGORIES = [
    "Electronics", "Fashion", "Home Appliances", "Beauty", "Books", "Sports",
    "Furniture", "Groceries", "Toys", "Health", "Automotive", "Garden", "Office",
    "Jewelry", "Pet Supplies", "Music", "Movies", "Gaming", "Travel", "Food"
]

BRAND_NAMES = [
    "Samsung", "Apple", "OnePlus", "Sony", "Dell", "HP", "Lenovo", "Canon",
    "Nike", "Adidas", "Puma", "Levis", "Ray-Ban", "Philips", "Bosch", "LG",
    "Whirlpool", "Havells", "Bajaj", "Godrej", "Zara", "Myntra", "Amazon", "Flipkart"
]

PAYMENT_METHODS = [
    "UPI", "Credit Card", "Debit Card", "Wallet", "Net Banking", "Cash On Delivery"
]

ORDER_STATUS_VALUES = ["Pending", "Packed", "Shipped", "Delivered", "Cancelled", "Returned"]

PAYMENT_STATUS_VALUES = ["Pending", "Success", "Failed", "Refunded"]

CUSTOMER_PERSONA_DISTRIBUTION = {
    "window": 0.20,
    "casual": 0.50,
    "regular": 0.20,
    "premium": 0.08,
    "vip": 0.02,
}

CUSTOMER_PERSONA_ORDER_RANGES = {
    "window": (0, 0),
    "casual": (1, 5),
    "regular": (6, 20),
    "premium": (21, 50),
    "vip": (51, 150),
}

CUSTOMER_PERSONA_PRICE_BIAS = {
    "window": 0.70,
    "casual": 0.85,
    "regular": 1.00,
    "premium": 1.45,
    "vip": 2.10,
}

CUSTOMER_PERSONA_TOP_UP_DISTRIBUTION = {
    "regular": 0.55,
    "premium": 0.30,
    "vip": 0.15,
}

ORDER_ITEM_COUNT_DISTRIBUTION = {1: 0.50, 2: 0.25, 3: 0.15, 4: 0.08, 5: 0.02}

ORDER_STATUS_DISTRIBUTION = {
    "Delivered": 0.75,
    "Pending": 0.08,
    "Packed": 0.05,
    "Shipped": 0.05,
    "Cancelled": 0.05,
    "Returned": 0.02,
}

PAYMENT_METHOD_DISTRIBUTION = {
    "UPI": 0.45,
    "Credit Card": 0.20,
    "Debit Card": 0.15,
    "Wallet": 0.10,
    "Net Banking": 0.05,
    "Cash On Delivery": 0.05,
}

SEASONAL_MONTH_WEIGHTS = {
    1: 1.8,
    3: 1.6,
    8: 1.7,
    10: 1.9,
    11: 2.2,
    12: 1.8,
}

DEFAULT_MONTH_WEIGHT = 1.0
MAX_ORDER_QUANTITY = 4

REVIEW_PROBABILITY = 0.35
REVIEW_RATING_DISTRIBUTION = {5: 0.45, 4: 0.32, 3: 0.15, 2: 0.05, 1: 0.03}
MIN_DELIVERY_DAYS = 2
MAX_DELIVERY_DAYS = 7
MIN_REVIEW_DELAY_DAYS = 1
MAX_REVIEW_DELAY_DAYS = 45
SECONDS_PER_DAY = 86_399

MIN_CURRENT_STOCK = 10
MAX_CURRENT_STOCK = 250
MIN_REORDER_LEVEL = 5
REORDER_LEVEL_RATIO = 0.20
VALID_RETURN_STOCK_STATUSES = {"Approved", "Completed"}

RETURN_REASONS = ["Damaged", "Wrong Item", "Not as described", "Late delivery", "Size issue"]

REVIEW_COMMENTS = [
    "Excellent product and fast delivery.", "Very satisfied with the purchase.",
    "Good quality, would buy again.", "Comfortable and durable.", "Value for money.",
    "Packaging could be better.", "Average quality but okay.", "Delivery was delayed.",
    "Would recommend to others.", "Great experience overall."
]
