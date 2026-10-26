USE olist_ecommerce;

SELECT
    DATE_FORMAT(
        STR_TO_DATE(order_purchase_timestamp, '%Y-%m-%d %H:%i:%s'),
        '%Y-%m'
    ) AS order_month,
    COUNT(*) AS total_orders,
    SUM(CASE
        WHEN order_status = 'canceled' THEN 1
        ELSE 0
    END) AS canceled_orders,
    ROUND(
        SUM(CASE
            WHEN order_status = 'canceled' THEN 1
            ELSE 0
        END) * 100.0 / COUNT(*),
        2
    ) AS cancellation_rate_pct
FROM orders
WHERE order_purchase_timestamp IS NOT NULL
  AND STR_TO_DATE(
      order_purchase_timestamp,
      '%Y-%m-%d %H:%i:%s'
  ) IS NOT NULL
GROUP BY order_month
ORDER BY order_month;