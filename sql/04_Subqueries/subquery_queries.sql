SELECT customer_id FROM orders WHERE total_amount > (SELECT AVG(total_amount) FROM orders);
