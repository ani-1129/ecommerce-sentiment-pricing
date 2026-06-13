#!/usr/bin/env python3
"""
Load enriched data into PostgreSQL (FREE)
"""

import json
import os
import redis
import psycopg2
from psycopg2 import sql
from datetime import datetime

# ═════════════════════════════════════════
# Configuration
# ═════════════════════════════════════════
# Redis connection
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
redis_client = redis.from_url(REDIS_URL)

# PostgreSQL connection (FREE)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:admin123@localhost:5432/ecommerce_db")
conn = psycopg2.connect(DATABASE_URL)

# ═════════════════════════════════════════
# Database Loading Function
# ═════════════════════════════════════════
def load_enriched_reviews():
    """Load enriched reviews from Redis Stream to PostgreSQL"""
    print("📥 Loading enriched reviews to PostgreSQL...")

    cursor = conn.cursor()

    try:
        # Read from enriched stream
        messages = redis_client.xread(streams={"enriched-data": "0"}, count=10)

        loaded_count = 0

        for stream_key, msg_list in messages:
            for msg in msg_list:
                data_json = msg["data"]
                enriched = json.loads(data_json)

                # Insert into PostgreSQL
                cursor.execute("""
                    INSERT INTO enriched_reviews 
                    (review_id, product_id, customer_id, rating, review_text, 
                     sentiment_score, sentiment_label, psychological_insights, 
                     confidence_score, enriched_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (review_id) DO UPDATE SET
                    sentiment_score = EXCLUDED.sentiment_score,
                    sentiment_label = EXCLUDED.sentiment_label,
                    psychological_insights = EXCLUDED.physiological_insights,
                    confidence_score = EXCLUDED.confidence_score,
                    enriched_at = EXCLUDED.enriched_at
                """, (
                    enriched["review_id"],
                    enriched["product_id"],
                    enriched["customer_id"],
                    enriched["rating"],
                    enriched["review_text"],
                    enriched["sentiment_score"],
                    enriched["sentiment_label"],
                    json.dumps(enriched["psychological_insights"]),
                    enriched["confidence_score"],
                    enriched["enriched_at"]
                ))

                loaded_count += 1
                print(f"✓ Loaded review: {enriched['review_id']}")

        # Commit changes
        conn.commit()
        print(f"✅ Batch complete! Loaded {loaded_count} reviews")

    except Exception as e:
        print(f"✗ Error loading to PostgreSQL: {e}")
        conn.rollback()

    finally:
        cursor.close()

# ═════════════════════════════════════════
# Main Execution
# ═════════════════════════════════════════
if __name__ == "__main__":
    load_enriched_reviews()