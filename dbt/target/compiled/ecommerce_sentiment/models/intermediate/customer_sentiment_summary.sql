
-- Customer Sentiment Summary (from enriched_reviews view)
WITH customer_reviews AS (
    SELECT
        customer_id,
        product_id,
        sentiment_label,
        sentiment_score,
        rating,
        confidence_score
    FROM "ecommerce_db"."public"."enriched_reviews"
),

customer_aggregates AS (
    SELECT
        customer_id,
        product_id,
        AVG(sentiment_score) AS avg_sentiment,
        COUNT(*) AS review_count,
        AVG(rating) AS avg_rating,
        AVG(confidence_score) AS avg_confidence,
        MAX(sentiment_score) AS max_sentiment,
        MIN(sentiment_score) AS min_sentiment
    FROM customer_reviews
    GROUP BY customer_id, product_id
)

SELECT
    customer_id,
    product_id,
    ROUND(avg_sentiment, 4) AS avg_sentiment,
    review_count,
    ROUND(avg_rating, 2) AS avg_rating,
    ROUND(avg_confidence, 4) AS avg_confidence,
    ROUND(max_sentiment, 4) AS max_sentiment,
    ROUND(min_sentiment, 4) AS min_sentiment,
    
    -- Sentiment velocity (change over time)
    ROUND(
        (max_sentiment - min_sentiment) / NULLIF(review_count, 0),
        4
    ) AS sentiment_velocity

FROM customer_aggregates