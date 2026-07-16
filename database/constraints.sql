
-- Additional constraints and business rules can be applied here.

ALTER TABLE customers
ADD CONSTRAINT chk_customers_status CHECK (status IN ('Active','Inactive','Suspended'));

ALTER TABLE orders
ADD CONSTRAINT chk_orders_status CHECK (order_status IN ('Pending','Packed','Shipped','Delivered','Cancelled','Returned'));
