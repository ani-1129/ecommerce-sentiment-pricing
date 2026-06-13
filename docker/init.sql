-- ═════════════════════════════════════════
-- E-Commerce Database Schema (FREE PostgreSQL)
-- ═════════════════════════════════════════

-- Table 1: Raw Reviews (Landing Zone)
CREATE TABLE raw_reviews (
    id SERIAL PRIMARY KEY,
    review_id VARCHAR(100) UNIQUE,
    product_id VARCHAR(100),
    customer_id VARCHAR(100),
    rating INTEGER,
    review_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sentiment_json JSONB
);

-- Table 2: Raw Orders (Landing Zone)
CREATE TABLE raw_orders (
    id SERIAL PRIMARY KEY,
    order_id VARCHAR(100) UNIQUE,
    product_id VARCHAR(100),
    customer_id VARCHAR(100),
    quantity INTEGER,
    price DECIMAL(10, 2),
    order_status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table 3: Enriched Reviews with Sentiment (Staging)
CREATE TABLE enriched_reviews (
    id SERIAL PRIMARY KEY,
    review_id VARCHAR(100) UNIQUE,
    product_id VARCHAR(100),
    customer_id VARCHAR(100),
    rating INTEGER,
    review_text TEXT,
    sentiment_score DECIMAL(5, 4),
    sentiment_label VARCHAR(50),
    psychological_insights JSONB,
    confidence_score DECIMAL(5, 4),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    enriched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table 4: Customer Sentiment Trends (Intermediate)
CREATE TABLE customer_sentiment_trends (
    customer_id VARCHAR(100),
    product_id VARCHAR(100),
    avg_sentiment DECIMAL(5, 4),
    sentiment_velocity DECIMAL(5, 4),
    review_count INTEGER,
    last_review_date TIMESTAMP,
    PRIMARY KEY (customer_id, product_id)
);

-- Table 5: Dynamic Pricing Recommendations (Mart)
CREATE TABLE pricing_recommendations (
    product_id VARCHAR(100) PRIMARY KEY,
    current_price DECIMAL(10, 2),
    recommended_price DECIMAL(10, 2),
    price_adjustment_pct DECIMAL(5, 4),
    sentiment_score DECIMAL(5, 4),
    confidence_level VARCHAR(50),
    recommendation_reason TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ═════════════════════════════════════════
-- Performance Indexes
-- ═════════════════════════════════════════
CREATE INDEX idx_reviews_product ON raw_reviews(product_id);
CREATE INDEX idx_reviews_customer ON raw_reviews(customer_id);
CREATE INDEX idx_enriched_sentiment ON enriched_reviews(sentiment_score);
CREATE INDEX idx_trends_customer ON customer_sentiment_trends(customer_id);

-- ═════════════════════════════════════════
-- Success Message
-- ═════════════════════════════════════════
COMMENT ON TABLE raw_reviews IS 'Landing zone for raw customer reviews';
COMMENT ON TABLE enriched_reviews IS 'Staging zone with AI-enriched sentiment data';
COMMENT ON TABLE pricing_recommendations IS 'Dynamic pricing recommendations';