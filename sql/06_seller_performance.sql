USE olist_ecommerce;

SELECT
    oi.seller_id,
    COUNT(*) AS total_items_sold,
    COUNT(DISTINCT oi.order_id) AS total_orders,
    ROUND(SUM(oi.price), 2) AS total_sales,
    ROUND(AVG(oi.price), 2) AS average_item_price

FROM order_items AS oi

JOIN sellers AS s
    ON oi.seller_id = s.seller_id

GROUP BY oi.seller_id

ORDER BY total_sales DESC;