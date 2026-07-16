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

RETURN_REASONS = ["Damaged", "Wrong Item", "Not as described", "Late delivery", "Size issue"]

REVIEW_COMMENTS = [
    "Excellent product and fast delivery.", "Very satisfied with the purchase.",
    "Good quality, would buy again.", "Comfortable and durable.", "Value for money.",
    "Packaging could be better.", "Average quality but okay.", "Delivery was delayed.",
    "Would recommend to others.", "Great experience overall."
]
