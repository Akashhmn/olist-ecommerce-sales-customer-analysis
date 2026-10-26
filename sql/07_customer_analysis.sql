USE olist_ecommerce;
-- CHECK TOTAL ORDERS  ------------------------------------
SELECT
    customer_id,
    COUNT(order_id) AS total_orders
FROM orders 
GROUP BY customer_id
ORDER BY total_orders DESC;

-- REPEATED ORDERS BY SINGLE CUSTOMER -----------------------------------------------------
USE olist_ecommerce;
SELECT
    c.customer_unique_id,
    COUNT(o.order_id) AS total_orders
FROM customers AS c
JOIN orders AS o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_unique_id
ORDER BY total_orders DESC;

-- REPEATED CUSTOMER PERENTAGE  ----------------------------------------------------
USE olist_ecommerce;
WITH customer_order_counts AS (
    SELECT
        c.customer_unique_id,
        COUNT(o.order_id) AS total_orders
    FROM customers AS c
    JOIN orders AS o
        ON c.customer_id = o.customer_id
    GROUP BY c.customer_unique_id
)

SELECT
    COUNT(*) AS total_unique_customers,

    SUM(
        CASE
            WHEN total_orders > 1 THEN 1
            ELSE 0
        END
    ) AS repeat_customers,

    SUM(
        CASE
            WHEN total_orders = 1 THEN 1
            ELSE 0
        END
    ) AS one_time_customers,

    ROUND(
        SUM(
            CASE
                WHEN total_orders > 1 THEN 1
                ELSE 0
            END
        ) * 100.0 / COUNT(*),
        2
    ) AS repeat_customer_percentage

FROM customer_order_counts;


-- FOR CTE PRACTICE   ------------------------------------------------------------------------------

USE olist_ecommerce;

WITH customer_order_counts AS (
    SELECT
        c.customer_unique_id,
        COUNT(o.order_id) AS total_orders
    FROM customers c
    JOIN orders o
        ON c.customer_id = o.customer_id
    GROUP BY c.customer_unique_id
)

SELECT
    COUNT(*) AS total_unique_customers,
    SUM(CASE WHEN total_orders > 1 THEN 1 ELSE 0 END)
        AS repeat_customers,
    SUM(CASE WHEN total_orders = 1 THEN 1 ELSE 0 END)
        AS one_time_customers,
    ROUND(
        SUM(CASE WHEN total_orders > 1 THEN 1 ELSE 0 END)
        * 100.0 / COUNT(*),
        2
    ) AS repeat_customer_percentage,
    ROUND(AVG(total_orders), 2) AS avg_orders_per_customer
FROM customer_order_counts;