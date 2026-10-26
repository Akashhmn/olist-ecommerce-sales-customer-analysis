USE olist_ecommerce;

SELECT
	review_score, 
    COUNT(*) AS total_reviews,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM reviews), 2) AS review_percentage
FROM reviews
WHERE review_score IS NOT NULL
GROUP BY review_score
ORDER BY review_score;

USE olist_ecommerce;
SELECT 
	COUNT(*) AS total_reviews,
    ROUND(AVG(review_score), 2) AS overall_average_rating
    FROM reviews
    WHERE review_score IS NOT NULL