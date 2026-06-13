
  
    

  create  table "ecommerce_db"."public"."pricing_recommendations__dbt_tmp"
  
  
    as
  
  (
    -- ═════════════════════════════════════════
-- Mart: Dynamic Pricing Recommendations
-- (100% FREE)
-- ═════════════════════════════════════════

WITH product_metrics AS (
    SELECT
        product_id,
        overall_sentiment_score,
        overall_rating,
        total_reviews,
        priority_score,
        sentiment_category
    FROM "ecommerce_db"."public"."product_sentiment_analysis"
),

order_metrics AS (
    SELECT
        product_id,
        AVG(price) AS avg_price,
        SUM(quantity) AS total_units_sold,
        COUNT(*) AS order_count
    FROM "ecommerce_db"."public"."raw_orders"
    GROUP BY product_id
)

SELECT
    p.product_id,
    
    -- Current price
    ROUND(o.avg_price, 2) AS current_price,
    
    -- Recommended price adjustment
    ROUND(
        o.avg_price * (1 + (p.overall_sentiment_score - 0.5) * 0.2),
        2
    ) AS recommended_price,
    
    -- Price adjustment percentage
    ROUND(
        ((o.avg_price * (1 + (p.overall_sentiment_score - 0.5) * 0.2)) - o.avg_price) / 
        NULLIF(o.avg_price, 0) * 100,
        2
    ) AS price_adjustment_pct,
    
    -- Sentiment metrics
    ROUND(p.overall_sentiment_score, 4) AS sentiment_score,
    p.overall_rating,
    p.total_reviews,
    
    -- Confidence level
    CASE
        WHEN p.total_reviews >= 10 THEN 'high'
        WHEN p.total_reviews >= 5 THEN 'medium'
        ELSE 'low'
    END AS confidence_level,
    
    -- Recommendation reason
    CASE
        WHEN p.sentiment_category = 'highly_positive' THEN 'Increase price due to high satisfaction'
        WHEN p.sentiment_category = 'positive' THEN 'Moderate price increase recommended'
        WHEN p.sentiment_category = 'neutral' THEN 'Maintain current price'
        WHEN p.sentiment_category = 'slightly_negative' THEN 'Small price decrease recommended'
        ELSE 'Significant price decrease needed'
    END AS recommendation_reason,
    
    -- Sales metrics
    o.total_units_sold,
    o.order_count,
    
    CURRENT_TIMESTAMP AS recommended_at

FROM product_metrics p
LEFT JOIN order_metrics o ON p.product_id = o.product_id
ORDER BY priority_score DESC
  );
  