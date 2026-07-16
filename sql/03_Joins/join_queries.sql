SELECT o.order_id, c.first_name, o.total_amount FROM orders o JOIN customers c ON c.customer_id = o.customer_id LIMIT 10;
