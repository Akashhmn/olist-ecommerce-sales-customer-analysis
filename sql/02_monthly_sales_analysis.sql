USE olist_ecommerce;

SELECT
    DATE_FORMAT(
        STR_TO_DATE(o.order_purchase_timestamp, '%Y-%m-%d %H:%i:%s'),
        '%Y-%m'
    ) AS sales_month,
    COUNT(*) AS total_orders,
    ROUND(SUM(p.order_payment_total), 2) AS monthly_revenue,
    ROUND(
        SUM(p.order_payment_total) / COUNT(*),
        2
    ) AS average_order_value
FROM orders AS o
JOIN (
    SELECT
        order_id,
        SUM(payment_value) AS order_payment_total
    FROM payments
    GROUP BY order_id
) AS p
    ON o.order_id = p.order_id
WHERE o.order_purchase_timestamp IS NOT NULL
  AND STR_TO_DATE(
      o.order_purchase_timestamp,
      '%Y-%m-%d %H:%i:%s'
  ) IS NOT NULL
GROUP BY sales_month
ORDER BY sales_month;