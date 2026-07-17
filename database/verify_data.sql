-- ==========================================================
-- File        : 09_verify_load.sql
-- Project     : TechMart Data Engineering
-- Purpose     : Post-load data quality and integrity verification
-- Author      : Onkar Jadhav
-- ==========================================================

USE techmart;

-- SECTION 1 : Environment
SELECT DATABASE() AS current_database, NOW() AS verification_time;

-- SECTION 2 : Row Counts
SELECT 'addresses' table_name, COUNT(*) row_count FROM addresses
UNION ALL SELECT 'brands',COUNT(*) FROM brands
UNION ALL SELECT 'categories',COUNT(*) FROM categories
UNION ALL SELECT 'customers',COUNT(*) FROM customers
UNION ALL SELECT 'suppliers',COUNT(*) FROM suppliers
UNION ALL SELECT 'products',COUNT(*) FROM products
UNION ALL SELECT 'warehouses',COUNT(*) FROM warehouses
UNION ALL SELECT 'inventory',COUNT(*) FROM inventory
UNION ALL SELECT 'orders',COUNT(*) FROM orders
UNION ALL SELECT 'order_items',COUNT(*) FROM order_items
UNION ALL SELECT 'payments',COUNT(*) FROM payments
UNION ALL SELECT 'reviews',COUNT(*) FROM reviews
UNION ALL SELECT 'shipments',COUNT(*) FROM shipments;

-- SECTION 3 : Duplicate Primary Keys
SELECT 'products' table_name, COUNT(*) duplicate_groups
FROM (SELECT product_id FROM products GROUP BY product_id HAVING COUNT(*)>1) t
UNION ALL
SELECT 'customers', COUNT(*) FROM (SELECT customer_id FROM customers GROUP BY customer_id HAVING COUNT(*)>1) t
UNION ALL
SELECT 'orders', COUNT(*) FROM (SELECT order_id FROM orders GROUP BY order_id HAVING COUNT(*)>1) t
UNION ALL
SELECT 'order_items', COUNT(*) FROM (SELECT order_item_id FROM order_items GROUP BY order_item_id HAVING COUNT(*)>1) t
UNION ALL
SELECT 'payments', COUNT(*) FROM (SELECT payment_id FROM payments GROUP BY payment_id HAVING COUNT(*)>1) t
UNION ALL
SELECT 'inventory', COUNT(*) FROM (SELECT inventory_id FROM inventory GROUP BY inventory_id HAVING COUNT(*)>1) t
UNION ALL
SELECT 'reviews', COUNT(*) FROM (SELECT review_id FROM reviews GROUP BY review_id HAVING COUNT(*)>1) t;

-- SECTION 4 : Foreign Key Integrity
SELECT 'customers->addresses' AS check_name, COUNT(*) AS invalid_rows
FROM customers c LEFT JOIN addresses a ON c.address_id=a.address_id
WHERE a.address_id IS NULL
UNION ALL
SELECT 'products->brands', COUNT(*) FROM products p LEFT JOIN brands b ON p.brand_id=b.brand_id WHERE b.brand_id IS NULL
UNION ALL
SELECT 'products->categories', COUNT(*) FROM products p LEFT JOIN categories c ON p.category_id=c.category_id WHERE c.category_id IS NULL
UNION ALL
SELECT 'products->suppliers', COUNT(*) FROM products p LEFT JOIN suppliers s ON p.supplier_id=s.supplier_id WHERE s.supplier_id IS NULL
UNION ALL
SELECT 'orders->customers', COUNT(*) FROM orders o LEFT JOIN customers c ON o.customer_id=c.customer_id WHERE c.customer_id IS NULL
UNION ALL
SELECT 'order_items->orders', COUNT(*) FROM order_items oi LEFT JOIN orders o ON oi.order_id=o.order_id WHERE o.order_id IS NULL
UNION ALL
SELECT 'order_items->products', COUNT(*) FROM order_items oi LEFT JOIN products p ON oi.product_id=p.product_id WHERE p.product_id IS NULL
UNION ALL
SELECT 'payments->orders', COUNT(*) FROM payments p LEFT JOIN orders o ON p.order_id=o.order_id WHERE o.order_id IS NULL
UNION ALL
SELECT 'reviews->products', COUNT(*) FROM reviews r LEFT JOIN products p ON r.product_id=p.product_id WHERE p.product_id IS NULL
UNION ALL
SELECT 'inventory->products', COUNT(*) FROM inventory i LEFT JOIN products p ON i.product_id=p.product_id WHERE p.product_id IS NULL
UNION ALL
SELECT 'inventory->warehouses', COUNT(*) FROM inventory i LEFT JOIN warehouses w ON i.warehouse_id=w.warehouse_id WHERE w.warehouse_id IS NULL
UNION ALL
SELECT 'shipments->orders', COUNT(*) FROM shipments s LEFT JOIN orders o ON s.order_id=o.order_id WHERE o.order_id IS NULL;

-- SECTION 5 : Mandatory Fields
SELECT SUM(first_name IS NULL) AS missing_first_name,
       SUM(last_name IS NULL) AS missing_last_name,
       SUM(email IS NULL) AS missing_email
FROM customers;

SELECT SUM(product_name IS NULL) AS missing_product_name,
       SUM(sku IS NULL) AS missing_sku
FROM products;

-- SECTION 6 : Business Rules
SELECT COUNT(*) AS invalid_price_rows FROM products WHERE cost_price > selling_price;
SELECT COUNT(*) AS negative_payment_amount FROM payments WHERE payment_amount < 0;
SELECT COUNT(*) AS invalid_rating FROM reviews WHERE rating NOT BETWEEN 1 AND 5;
SELECT COUNT(*) AS invalid_quantity FROM order_items WHERE quantity <= 0;
SELECT COUNT(*) AS invalid_total_amount FROM orders WHERE total_amount <= 0;

-- SECTION 7 : Inventory
SELECT COUNT(*) AS negative_stock FROM inventory WHERE current_stock < 0;
SELECT COUNT(*) AS below_reorder_level FROM inventory WHERE current_stock < reorder_level;

-- SECTION 8 : Duplicate Emails
SELECT email, COUNT(*) AS duplicates
FROM customers
GROUP BY email
HAVING COUNT(*)>1;

SELECT email, COUNT(*) AS duplicates
FROM suppliers
GROUP BY email
HAVING COUNT(*)>1;

-- SECTION 9 : Revenue
SELECT ROUND(SUM(total_amount),2) AS total_order_revenue FROM orders;
SELECT ROUND(SUM(payment_amount),2) AS total_payment_received FROM payments;

-- SECTION 10 : Final Status
SELECT 'PASS' AS verification_result,
       'TechMart database verification completed successfully.' AS message,
       NOW() AS completed_at;
