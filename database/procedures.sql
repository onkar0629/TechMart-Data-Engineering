
DELIMITER $$

CREATE PROCEDURE sp_get_sales_by_period(IN start_date DATE, IN end_date DATE)
BEGIN
    SELECT
        DATE(order_date) AS order_day,
        COUNT(*) AS order_count,
        ROUND(SUM(total_amount), 2) AS revenue
    FROM orders
    WHERE order_date BETWEEN start_date AND end_date
    GROUP BY DATE(order_date)
    ORDER BY order_day;
END$$

DELIMITER ;
