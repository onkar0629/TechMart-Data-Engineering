
-- ==========================================================
-- TechMart Database Schema
-- MySQL 8.x compatible
-- ==========================================================

DROP DATABASE IF EXISTS techmart;
CREATE DATABASE techmart;
USE techmart;

CREATE TABLE addresses (
    address_id INT AUTO_INCREMENT PRIMARY KEY,
    address_line1 VARCHAR(255) NOT NULL,
    address_line2 VARCHAR(255) DEFAULT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    postal_code VARCHAR(20) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_addresses_postal_code CHECK (CHAR_LENGTH(postal_code) >= 3)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(20) DEFAULT NULL UNIQUE,
    gender ENUM('Male','Female','Other','Prefer not to say') NOT NULL DEFAULT 'Prefer not to say',
    date_of_birth DATE DEFAULT NULL,
    registration_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status ENUM('Active','Inactive','Suspended') NOT NULL DEFAULT 'Active',
    address_id INT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_customers_address_id FOREIGN KEY (address_id) REFERENCES addresses(address_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL UNIQUE,
    parent_category_id INT DEFAULT NULL,
    description VARCHAR(500) DEFAULT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_categories_parent_category_id FOREIGN KEY (parent_category_id) REFERENCES categories(category_id)
        ON UPDATE CASCADE ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE brands (
    brand_id INT AUTO_INCREMENT PRIMARY KEY,
    brand_name VARCHAR(100) NOT NULL UNIQUE,
    brand_origin VARCHAR(100) DEFAULT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE suppliers (
    supplier_id INT AUTO_INCREMENT PRIMARY KEY,
    supplier_name VARCHAR(200) NOT NULL,
    contact_person VARCHAR(150) DEFAULT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(20) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    rating DECIMAL(3,2) DEFAULT 0.00,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_suppliers_rating CHECK (rating BETWEEN 0.00 AND 5.00)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(250) NOT NULL,

    brand_id INT NOT NULL,
    category_id INT NOT NULL,
    supplier_id INT NOT NULL,

    sku VARCHAR(100) NOT NULL UNIQUE,

    description TEXT,

    cost_price DECIMAL(10,2) NOT NULL,
    selling_price DECIMAL(10,2) NOT NULL,

    weight_grams INT NOT NULL,
    warranty_months INT NOT NULL DEFAULT 12,

    is_active BOOLEAN NOT NULL DEFAULT TRUE,

    popularity INT NOT NULL DEFAULT 0,

    FOREIGN KEY (brand_id) REFERENCES brands(brand_id),
    FOREIGN KEY (category_id) REFERENCES categories(category_id),
    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id),

    CHECK (cost_price > 0),
    CHECK (selling_price > 0),
    CHECK (cost_price <= selling_price)
);

CREATE TABLE warehouses (
    warehouse_id INT AUTO_INCREMENT PRIMARY KEY,
    warehouse_name VARCHAR(150) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    capacity_units INT NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE inventory (
    inventory_id INT AUTO_INCREMENT PRIMARY KEY,

    product_id INT NOT NULL,

    warehouse_id INT NOT NULL,

    opening_stock INT NOT NULL,

    units_sold INT NOT NULL DEFAULT 0,

    units_returned INT NOT NULL DEFAULT 0,

    current_stock INT NOT NULL,

    stock_quantity INT NOT NULL,

    reorder_level INT NOT NULL DEFAULT 0,

    last_updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uq_inventory_product_warehouse
        UNIQUE (product_id, warehouse_id),

    FOREIGN KEY (product_id)
        REFERENCES products(product_id),

    FOREIGN KEY (warehouse_id)
        REFERENCES warehouses(warehouse_id),

    CHECK (opening_stock >= 0),

    CHECK (units_sold >= 0),

    CHECK (units_returned >= 0),

    CHECK (current_stock >= 0),

    CHECK (stock_quantity >= 0),

    CHECK (reorder_level >= 0)
);

CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,

    customer_id INT NOT NULL,

    order_date DATETIME NOT NULL,

    order_status ENUM(
        'Pending',
        'Packed',
        'Shipped',
        'Delivered',
        'Cancelled',
        'Returned'
    ) NOT NULL,

    payment_status ENUM(
        'Pending',
        'Paid',
        'Failed',
        'Refunded'
    ) NOT NULL,

    total_amount DECIMAL(12,2) NOT NULL,

    shipping_address_id INT NOT NULL,

    billing_address_id INT NOT NULL,

    FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id),

    FOREIGN KEY (shipping_address_id)
        REFERENCES addresses(address_id),

    FOREIGN KEY (billing_address_id)
        REFERENCES addresses(address_id),

    CHECK (total_amount >= 0)
);

CREATE TABLE order_items (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,

    order_id INT NOT NULL,

    product_id INT NOT NULL,

    quantity INT NOT NULL,

    unit_price DECIMAL(10,2) NOT NULL,

    discount_percentage DECIMAL(5,2) NOT NULL DEFAULT 0.00,

    FOREIGN KEY (order_id)
        REFERENCES orders(order_id)
        ON DELETE CASCADE,

    FOREIGN KEY (product_id)
        REFERENCES products(product_id),

    CHECK (quantity > 0),

    CHECK (unit_price >= 0),

    CHECK (discount_percentage BETWEEN 0 AND 100)
);

CREATE TABLE payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,

    order_id INT NOT NULL,

    payment_method ENUM(
        'UPI',
        'Credit Card',
        'Debit Card',
        'Wallet',
        'Net Banking',
        'Cash On Delivery'
    ) NOT NULL,

    payment_date DATETIME NOT NULL,

    payment_status ENUM(
        'Pending',
        'Success',
        'Failed',
        'Refunded'
    ) NOT NULL,

    payment_amount DECIMAL(12,2) NOT NULL,

    transaction_reference VARCHAR(100) NOT NULL UNIQUE,

    gateway_response VARCHAR(255),

    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (order_id)
        REFERENCES orders(order_id)
        ON DELETE CASCADE,

    CHECK (payment_amount >= 0)
);

CREATE TABLE reviews (
    review_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    product_id INT NOT NULL,
    rating TINYINT NOT NULL,
    review_comment TEXT DEFAULT NULL,
    review_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_verified TINYINT(1) NOT NULL DEFAULT 0,
    CONSTRAINT fk_reviews_customer_id FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    CONSTRAINT fk_reviews_product_id FOREIGN KEY (product_id) REFERENCES products(product_id),
    CONSTRAINT chk_reviews_rating CHECK (rating BETWEEN 1 AND 5)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE shipments (
    shipment_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    warehouse_id INT NOT NULL,
    tracking_number VARCHAR(100) NOT NULL UNIQUE,
    shipment_status ENUM('Pending','Packed','In Transit','Delivered','Failed') NOT NULL DEFAULT 'Pending',
    shipped_at DATETIME DEFAULT NULL,
    delivered_at DATETIME DEFAULT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_shipments_order_id FOREIGN KEY (order_id) REFERENCES orders(order_id),
    CONSTRAINT fk_shipments_warehouse_id FOREIGN KEY (warehouse_id) REFERENCES warehouses(warehouse_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE returns (
    return_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    return_reason VARCHAR(255) NOT NULL,
    return_status ENUM('Requested','Approved','Rejected','Completed') NOT NULL DEFAULT 'Requested',
    return_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    refund_amount DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    CONSTRAINT fk_returns_order_id FOREIGN KEY (order_id) REFERENCES orders(order_id),
    CONSTRAINT fk_returns_product_id FOREIGN KEY (product_id) REFERENCES products(product_id),
    CONSTRAINT chk_returns_refund_amount CHECK (refund_amount >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE employees (
    employee_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(20) DEFAULT NULL,
    role VARCHAR(100) NOT NULL,
    warehouse_id INT DEFAULT NULL,
    hire_date DATE NOT NULL,
    is_active TINYINT(1) NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_employees_warehouse_id FOREIGN KEY (warehouse_id) REFERENCES warehouses(warehouse_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE coupons (
    coupon_id INT AUTO_INCREMENT PRIMARY KEY,
    coupon_code VARCHAR(50) NOT NULL UNIQUE,
    discount_percent DECIMAL(5,2) NOT NULL DEFAULT 0.00,
    valid_from DATETIME NOT NULL,
    valid_to DATETIME NOT NULL,
    is_active TINYINT(1) NOT NULL DEFAULT 1,
    min_order_amount DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_coupons_discount_percent CHECK (discount_percent BETWEEN 0.00 AND 100.00),
    CONSTRAINT chk_coupons_dates CHECK (valid_to >= valid_from)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE wishlists (
    wishlist_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    product_id INT NOT NULL,
    added_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_wishlists_customer_id FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    CONSTRAINT fk_wishlists_product_id FOREIGN KEY (product_id) REFERENCES products(product_id),
    CONSTRAINT uq_wishlists_customer_product UNIQUE (customer_id, product_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE shopping_cart (
    cart_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_shopping_cart_customer_id FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE shopping_cart_items (
    cart_item_id INT AUTO_INCREMENT PRIMARY KEY,
    cart_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    added_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_shopping_cart_items_cart_id FOREIGN KEY (cart_id) REFERENCES shopping_cart(cart_id) ON DELETE CASCADE,
    CONSTRAINT fk_shopping_cart_items_product_id FOREIGN KEY (product_id) REFERENCES products(product_id),
    CONSTRAINT chk_shopping_cart_items_quantity CHECK (quantity > 0),
    CONSTRAINT uq_shopping_cart_items_cart_product UNIQUE (cart_id, product_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- ==========================================================
-- Seed Warehouses (required before importing inventory.csv)
-- ==========================================================
INSERT INTO warehouses
(warehouse_name, city, state, country, capacity_units)
VALUES
('Mumbai Warehouse','Mumbai','Maharashtra','India',100000),
('Pune Warehouse','Pune','Maharashtra','India',80000),
('Bengaluru Warehouse','Bengaluru','Karnataka','India',120000),
('Delhi Warehouse','New Delhi','Delhi','India',90000);
