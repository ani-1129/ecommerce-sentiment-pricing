-- ═════════════════════════════════════════
-- Mart: Product Sentiment Analysis
-- (100% FREE)
-- ═════════════════════════════════════════

WITH product_sentiments AS (
    SELECT
        customer_id,
        product_id,
        avg_sentiment,
        review_count,
        avg_rating,
        avg_confidence,
        sentiment_velocity
    FROM {{ ref('customer_sentiment_summary') }}
),

product_aggregates AS (
    SELECT
        product_id,
        AVG(avg_sentiment) AS overall_sentiment,
        SUM(review_count) AS total_reviews,
        AVG(avg_rating) AS overall_rating,
        AVG(avg_confidence) AS overall_confidence,
        AVG(sentiment_velocity) AS sentiment_velocity,
        COUNT(DISTINCT customer_id) AS unique_customers
    FROM product_sentiments
    GROUP BY product_id
)

SELECT
    product_id,
    
    -- Overall metrics
    ROUND(overall_sentiment, 4) AS overall_sentiment_score,
    total_reviews,
    ROUND(overall_rating, 2) AS overall_rating,
    ROUND(overall_confidence, 4) AS overall_confidence,
    
    -- Sentiment distribution
    ROUND(sentiment_velocity, 4) AS sentiment_velocity,
    
    -- Customer engagement
    unique_customers,
    
    -- Sentiment category
    CASE
        WHEN overall_sentiment >= 0.7 THEN 'highly_positive'
        WHEN overall_sentiment >= 0.4 THEN 'positive'
        WHEN overall_sentiment >= 0.3 THEN 'neutral'
        WHEN overall_sentiment >= 0.1 THEN 'slightly_negative'
        ELSE 'negative'
    END AS sentiment_category,
    
    -- Priority score (for recommendations)
    ROUND(
        (overall_sentiment * 0.6) + 
        (overall_rating / 5.0 * 0.4),
        4
    ) AS priority_score,
    
    CURRENT_TIMESTAMP AS analyzed_at

FROM product_aggregates
ORDER BY overall_sentiment DESC