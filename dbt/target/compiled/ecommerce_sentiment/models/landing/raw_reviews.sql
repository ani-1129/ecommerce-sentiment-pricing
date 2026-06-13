-- Raw Reviews Landing Zone (No transformation - just copy from source)
SELECT
    review_id,
    product_id,
    customer_id,
    rating,
    review_text,
    review_date,
    verified_purchase,
    loaded_at,
    sentiment_json
FROM "ecommerce_db"."public"."raw_reviews"