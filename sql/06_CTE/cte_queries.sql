WITH top_customers AS (SELECT customer_id, SUM(total_amount) AS spend FROM orders GROUP BY customer_id) SELECT * FROM top_customers LIMIT 10;
