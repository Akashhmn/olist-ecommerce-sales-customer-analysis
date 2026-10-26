USE olist_ecommerce;
-- LATE DELIVERY ORDERS & PERCENTAGE
SELECT
    COUNT(*) AS delivered_orders_analyzed,

    SUM(
        CASE
            WHEN STR_TO_DATE(order_delivered_customer_date, '%Y-%m-%d %H:%i:%s')
                > STR_TO_DATE(order_estimated_delivery_date, '%Y-%m-%d %H:%i:%s')
            THEN 1
            ELSE 0
        END
    ) AS late_delivered_orders,

    SUM(
        CASE
            WHEN STR_TO_DATE(order_delivered_customer_date, '%Y-%m-%d %H:%i:%s')
               <= STR_TO_DATE(order_estimated_delivery_date, '%Y-%m-%d %H:%i:%s')
            THEN 1
            ELSE 0
        END
    ) AS on_time_or_early_orders,

    ROUND(
        SUM(
            CASE
                WHEN STR_TO_DATE(order_delivered_customer_date, '%Y-%m-%d %H:%i:%s')
                   > STR_TO_DATE(order_estimated_delivery_date, '%Y-%m-%d %H:%i:%s')
                THEN 1
                ELSE 0
            END
        ) * 100.0 / COUNT(*),
        2
    ) AS late_delivery_percentage,

    ROUND(
        AVG(
            DATEDIFF(
                STR_TO_DATE(order_delivered_customer_date, '%Y-%m-%d %H:%i:%s'),
                STR_TO_DATE(order_purchase_timestamp, '%Y-%m-%d %H:%i:%s')
            )
        ),
        2
    ) AS avg_actual_delivery_days,

    ROUND(
        AVG(
            DATEDIFF(
                STR_TO_DATE(order_estimated_delivery_date, '%Y-%m-%d %H:%i:%s'),
                STR_TO_DATE(order_purchase_timestamp, '%Y-%m-%d %H:%i:%s')
            )
        ),
        2
    ) AS avg_estimated_delivery_days

FROM orders
WHERE order_status = 'delivered'
  AND order_delivered_customer_date IS NOT NULL
  AND order_estimated_delivery_date IS NOT NULL
  AND order_purchase_timestamp IS NOT NULL
  AND STR_TO_DATE(order_delivered_customer_date, '%Y-%m-%d %H:%i:%s') IS NOT NULL
  AND STR_TO_DATE(order_estimated_delivery_date, '%Y-%m-%d %H:%i:%s') IS NOT NULL
  AND STR_TO_DATE(order_purchase_timestamp, '%Y-%m-%d %H:%i:%s') IS NOT NULL;


USE olist_ecommerce;
-- LATE DELIVERY ORDERS BY MONTHS
SELECT
    DATE_FORMAT(
        STR_TO_DATE(order_purchase_timestamp, '%Y-%m-%d %H:%i:%s'),
        '%Y-%m'
    ) AS purchase_month,

    COUNT(*) AS delivered_orders,

    SUM(
        CASE
            WHEN STR_TO_DATE(order_delivered_customer_date, '%Y-%m-%d %H:%i:%s')
               > STR_TO_DATE(order_estimated_delivery_date, '%Y-%m-%d %H:%i:%s')
            THEN 1
            ELSE 0
        END
    ) AS late_delivered_orders,

    ROUND(
        SUM(
            CASE
                WHEN STR_TO_DATE(order_delivered_customer_date, '%Y-%m-%d %H:%i:%s')
                   > STR_TO_DATE(order_estimated_delivery_date, '%Y-%m-%d %H:%i:%s')
                THEN 1
                ELSE 0
            END
        ) * 100.0 / COUNT(*),
        2
    ) AS late_delivery_percentage

FROM orders

WHERE order_status = 'delivered'
  AND order_purchase_timestamp IS NOT NULL
  AND order_delivered_customer_date IS NOT NULL
  AND order_estimated_delivery_date IS NOT NULL
  AND STR_TO_DATE(order_purchase_timestamp, '%Y-%m-%d %H:%i:%s') IS NOT NULL
  AND STR_TO_DATE(order_delivered_customer_date, '%Y-%m-%d %H:%i:%s') IS NOT NULL
  AND STR_TO_DATE(order_estimated_delivery_date, '%Y-%m-%d %H:%i:%s') IS NOT NULL

GROUP BY purchase_month
ORDER BY purchase_month;

-- AVG DELAY DAYS
SELECT
    COUNT(*) AS late_orders_analyzed,

    ROUND(
        AVG(
            DATEDIFF(
                STR_TO_DATE(order_delivered_customer_date, '%Y-%m-%d %H:%i:%s'),
                STR_TO_DATE(order_estimated_delivery_date, '%Y-%m-%d %H:%i:%s')
            )
        ),
        2
    ) AS avg_delay_days,

    MAX(
        DATEDIFF(
            STR_TO_DATE(order_delivered_customer_date, '%Y-%m-%d %H:%i:%s'),
            STR_TO_DATE(order_estimated_delivery_date, '%Y-%m-%d %H:%i:%s')
        )
    ) AS maximum_delay_days

FROM orders

WHERE order_status = 'delivered'
  AND order_delivered_customer_date IS NOT NULL
  AND order_estimated_delivery_date IS NOT NULL
  AND STR_TO_DATE(order_delivered_customer_date, '%Y-%m-%d %H:%i:%s') IS NOT NULL
  AND STR_TO_DATE(order_estimated_delivery_date, '%Y-%m-%d %H:%i:%s') IS NOT NULL
  AND STR_TO_DATE(order_delivered_customer_date, '%Y-%m-%d %H:%i:%s')
      > STR_TO_DATE(order_estimated_delivery_date, '%Y-%m-%d %H:%i:%s');