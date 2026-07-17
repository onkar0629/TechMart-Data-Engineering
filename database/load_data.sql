-- ==========================================================
-- 08_load_data.sql
-- TechMart Data Import Script (macOS Absolute Paths)
-- ==========================================================

USE techmart;

SET FOREIGN_KEY_CHECKS = 0;

LOAD DATA LOCAL INFILE '/Users/onkar/Documents/TechMart-Data-Engineering/generator/output/addresses.csv'
INTO TABLE addresses
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(address_id,address_line1,address_line2,city,state,country,postal_code);

LOAD DATA LOCAL INFILE '/Users/onkar/Documents/TechMart-Data-Engineering/generator/output/categories.csv'
INTO TABLE categories
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(category_id,category_name,parent_category_id,description);

LOAD DATA LOCAL INFILE '/Users/onkar/Documents/TechMart-Data-Engineering/generator/output/brands.csv'
INTO TABLE brands
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(brand_id,brand_name,brand_origin);

LOAD DATA LOCAL INFILE '/Users/onkar/Documents/TechMart-Data-Engineering/generator/output/suppliers.csv'
INTO TABLE suppliers
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(supplier_id,supplier_name,contact_person,email,phone,city,state,country,rating);

LOAD DATA LOCAL INFILE '/Users/onkar/Documents/TechMart-Data-Engineering/generator/output/customers.csv'
INTO TABLE customers
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(customer_id,first_name,last_name,email,phone,gender,date_of_birth,registration_date,status,address_id);

LOAD DATA LOCAL INFILE '/Users/onkar/Documents/TechMart-Data-Engineering/generator/output/products.csv'
INTO TABLE products
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(product_id,product_name,brand_id,category_id,supplier_id,sku,description,cost_price,selling_price,weight_grams,warranty_months,is_active,popularity);

LOAD DATA LOCAL INFILE '/Users/onkar/Documents/TechMart-Data-Engineering/generator/output/orders.csv'
INTO TABLE orders
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(order_id,customer_id,order_date,order_status,payment_status,total_amount,shipping_address_id,billing_address_id);

LOAD DATA LOCAL INFILE '/Users/onkar/Documents/TechMart-Data-Engineering/generator/output/order_items.csv'
INTO TABLE order_items
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(order_item_id,order_id,product_id,quantity,unit_price,discount_percentage);

LOAD DATA LOCAL INFILE '/Users/onkar/Documents/TechMart-Data-Engineering/generator/output/payments.csv'
INTO TABLE payments
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(payment_id,order_id,payment_method,payment_date,payment_status,payment_amount,transaction_reference);

LOAD DATA LOCAL INFILE '/Users/onkar/Documents/TechMart-Data-Engineering/generator/output/reviews.csv'
INTO TABLE reviews
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(review_id,customer_id,product_id,rating,review_comment,review_date,is_verified);

LOAD DATA LOCAL INFILE '/Users/onkar/Documents/TechMart-Data-Engineering/generator/output/inventory.csv'
INTO TABLE inventory
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(inventory_id,product_id,warehouse_id,opening_stock,units_sold,units_returned,current_stock,stock_quantity,reorder_level);

LOAD DATA LOCAL INFILE '/Users/onkar/Documents/TechMart-Data-Engineering/generator/output/shipments.csv'
INTO TABLE shipments
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(shipment_id,order_id,warehouse_id,tracking_number,shipment_status,shipped_at,delivered_at);

SET FOREIGN_KEY_CHECKS = 1;

SELECT 'TechMart data import completed successfully.' AS status;