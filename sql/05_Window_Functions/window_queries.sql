SELECT order_id, total_amount, RANK() OVER (ORDER BY total_amount DESC) AS ranking FROM orders LIMIT 10;
