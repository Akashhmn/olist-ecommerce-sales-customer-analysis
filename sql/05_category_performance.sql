USE olist_ecommerce;

SELECT
    COALESCE(ct.product_category_name_english, 'Unknown') AS product_category,
    COUNT(*) AS total_items_sold,
    COUNT(DISTINCT oi.order_id) AS total_orders,
    ROUND(SUM(oi.price), 2) AS total_sales,
    ROUND(AVG(oi.price), 2) AS average_item_price

FROM order_items AS oi

JOIN products AS p
    ON oi.product_id = p.product_id

LEFT JOIN category_translation AS ct
    ON p.product_category_name = ct.product_category_name

GROUP BY
    COALESCE(ct.product_category_name_english, 'Unknown')

ORDER BY total_sales DESC;