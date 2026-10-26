USE olist_ecommerce;

-- CHECK ALL DATA -------------------------------------
SELECT 'customers' AS table_name, COUNT(*) AS total_rows FROM customers
UNION ALL
SELECT 'orders', COUNT(*) FROM orders
UNION ALL
SELECT 'order_items', COUNT(*) FROM order_items
UNION ALL
SELECT 'payments', COUNT(*) FROM payments
UNION ALL
SELECT 'products', COUNT(*) FROM products
UNION ALL
SELECT 'reviews', COUNT(*) FROM reviews
UNION ALL
SELECT 'sellers', COUNT(*) FROM sellers
UNION ALL
SELECT 'category_translation', COUNT(*) FROM category_translation;

-- --  VALIDATE RELATIONSHIP  ---------------------------------
-- 1. Order items without a matching order
SELECT COUNT(*) AS invalid_rows
FROM order_items oi
LEFT JOIN orders o ON oi.order_id = o.order_id
WHERE o.order_id IS NULL
UNION ALL

-- 2. Order items without a matching product
SELECT COUNT(*) AS invalid_rows
FROM order_items oi
LEFT JOIN products p ON oi.product_id = p.product_id
WHERE p.product_id IS NULL
UNION ALL

-- 3. Order items without a matching seller
SELECT COUNT(*) AS invalid_rows
FROM order_items oi
LEFT JOIN sellers s ON oi.seller_id = s.seller_id
WHERE s.seller_id IS NULL
UNION ALL

-- 4. Orders without a matching customer
SELECT COUNT(*) AS invalid_rows
FROM orders o
LEFT JOIN customers c ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL
UNION ALL

-- 5. Payments without a matching order
SELECT COUNT(*) AS invalid_rows
FROM payments pay
LEFT JOIN orders o ON pay.order_id = o.order_id
WHERE o.order_id IS NULL
UNION ALL

-- 6. Reviews without a matching order
SELECT COUNT(*) AS invalid_rows
FROM reviews r
LEFT JOIN orders o ON r.order_id = o.order_id
WHERE o.order_id IS NULL; 


USE olist_ecommerce;
--   DUPLICATE COUNT ------------------------------------------
SELECT 'customers.customer_id' AS checked_column,
       COUNT(*) - COUNT(DISTINCT customer_id) AS duplicate_count
FROM customers

UNION ALL

SELECT 'orders.order_id',
       COUNT(*) - COUNT(DISTINCT order_id)
FROM orders

UNION ALL

SELECT 'products.product_id',
       COUNT(*) - COUNT(DISTINCT product_id)
FROM products

UNION ALL

SELECT 'sellers.seller_id',
       COUNT(*) - COUNT(DISTINCT seller_id)
FROM sellers

UNION ALL

SELECT 'category_translation.product_category_name',
       COUNT(*) - COUNT(DISTINCT product_category_name)
FROM category_translation;

--  DESCRIBE ---------------------------------------
DESCRIBE orders;
DESCRIBE payments;