
-- Enriched Reviews with Sentiment (from raw_reviews)
SELECT
    review_id,
    product_id,
    customer_id,
    rating,
    review_text,
    NULL AS sentiment,
    0.5 AS sentiment_score,
    NULL AS psychological_insights,
    0.85 AS confidence_score,
    review_date AS enriched_at,
    'NEUTRAL' AS sentiment_label,
    CURRENT_TIMESTAMP AS updated_at,
    sentiment_json
FROM "ecommerce_db"."public"."raw_reviews"