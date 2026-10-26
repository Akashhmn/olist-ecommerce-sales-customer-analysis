USE olist_ecommerce;

SELECT
    payment_type,
    COUNT(*) AS total_payment_records,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(payment_value), 2) AS total_payment_value,
    ROUND(AVG(payment_value), 2) AS average_payment_value,
    ROUND(SUM(payment_value) * 100.0 / (SELECT SUM(payment_value) FROM payments), 2) AS payment_value_share_pct 

FROM payments

GROUP BY payment_type

ORDER BY total_payment_value DESC;
