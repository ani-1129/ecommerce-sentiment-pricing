"""
LLM Enricher - Sentiment Analysis with Ollama
(100% FREE - No API costs!)
"""

import redis
import json
import psycopg2
import ollama
import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class LLMSentimentEnricher:
    """Analyzes review sentiment using Ollama LLM"""
    
    def __init__(self):
        """Initialize connections"""
        
        # Redis connection
        self.redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
        
        # PostgreSQL connection
        self.pg_client = psycopg2.connect(
            host='localhost',
            port=5432,
            user='admin',
            password='admin123',
            database='ecommerce_db'
        )
        
        print("✓ Connected to Redis and PostgreSQL")
    
    def analyze_sentiment(self, review_text):
        """Use Ollama to analyze sentiment"""
        
        try:
            # Call Ollama LLM
            response = ollama.chat(
                model='llama3.2',
                messages=[
                    {
                        'role': 'user',
                        'content': f'Analyze the sentiment of this review. Return only: POSITIVE, NEGATIVE, or NEUTRAL. Provide a brief explanation.\n\nReview: {review_text}'
                    }
                ]
            )
            
            # Extract sentiment and explanation
            content = response['message']['content'].strip().upper()
            
            # Parse sentiment
            if 'POSITIVE' in content:
                sentiment = 'POSITIVE'
                score = 1.0
            elif 'NEGATIVE' in content:
                sentiment = 'NEGATIVE'
                score = 0.0
            else:
                sentiment = 'NEUTRAL'
                score = 0.5
            
            # Extract psychological insights
            insights = {
                'sentiment': sentiment,
                'explanation': content,
                'confidence': 0.85  # Default confidence
            }
            
            return sentiment, score, json.dumps(insights)
            
        except Exception as e:
            print(f"✗ Ollama error: {e}")
            return 'NEUTRAL', 0.5, json.dumps({'sentiment': 'NEUTRAL', 'explanation': 'Error analyzing', 'confidence': 0.0})
    
    def save_to_raw_reviews(self, review_data):
        """Save raw review to landing zone table"""
        
        try:
            cursor = self.pg_client.cursor()
            
            cursor.execute("""
                INSERT INTO raw_reviews (
                    review_id, product_id, customer_id, rating, review_text, sentiment_json
                ) VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (review_id) DO NOTHING
            """, (
                review_data['review_id'],
                review_data['order_id'],  # Using order_id as product_id
                review_data['order_id'],  # customer_id
                review_data['rating'],
                review_data['review_text'],
                json.dumps({'raw': True, 'timestamp': datetime.now().isoformat()})
            ))
            
            self.pg_client.commit()
            cursor.close()
            
            print(f"✓ Saved to raw_reviews: {review_data['review_id']}")
            
            return True
            
        except Exception as e:
            print(f"✗ Error saving to raw_reviews: {e}")
            return False
    
    def save_to_enriched_reviews(self, enriched_data):
        """Save enriched review to staging table"""
        
        try:
            cursor = self.pg_client.cursor()
            
            # FIXED: Removed ON CONFLICT clause (causes tuple error)
            cursor.execute("""
                INSERT INTO enriched_reviews (
                    review_id, product_id, customer_id, rating, review_text,
                    sentiment_score, sentiment_label, psychological_insights, confidence_score
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                enriched_data['review_id'],
                enriched_data['order_id'],
                enriched_data['order_id'],
                enriched_data['rating'],
                enriched_data['review_text'],
                enriched_data['sentiment_score'],
                enriched_data['sentiment_label'],
                enriched_data['psychological_insights'],
                enriched_data['confidence_score']
            ))
            
            self.pg_client.commit()
            cursor.close()
            
            print(f"✓ Saved to enriched_reviews: {enriched_data['review_id']} [Sentiment: {enriched_data['sentiment_label']}]")
            
            return True
            
        except Exception as e:
            print(f"✗ Error saving to enriched_reviews: {e}")
            return False
    
    def process_review(self, review_data):
        """Process a single review with sentiment analysis"""
        
        # Get review text
        review_text = review_data.get('review_text', '')
        
        print(f"\n🧪 Analyzing review: {review_text[:60]}...")
        
        # Analyze sentiment
        sentiment, score, insights = self.analyze_sentiment(review_text)
        
        # Create enriched data
        enriched = {
            'review_id': review_data['review_id'],
            'order_id': review_data['order_id'],
            'rating': review_data['rating'],
            'review_text': review_text,
            'sentiment_label': sentiment,
            'sentiment_score': score,
            'psychological_insights': insights,
            'confidence_score': 0.85
        }
        
        print(f"🤖 Sentiment: {sentiment} (Score: {score})")
        
        return enriched
    
    def process_stream(self, stream_name='ecommerce_data', count=40):
        """Process all messages from Redis stream"""
        
        print(f"🚀 Processing {count} messages from {stream_name}...")
        
        # Read from stream
        messages = self.redis_client.xrevrange(stream_name, '+', '-', count=count)
        
        processed_count = 0
        review_count = 0
        
        for message_id, message_data in messages:
            # Parse JSON data
            try:
                data = json.loads(message_data['data'])
                
                # Check if it's a review
                if 'review_text' in data:
                    review_count += 1
                    
                    # Save to raw_reviews (landing zone)
                    self.save_to_raw_reviews(data)
                    
                    # Process with sentiment analysis
                    enriched = self.process_review(data)
                    
                    # Save to enriched_reviews (staging)
                    self.save_to_enriched_reviews(enriched)
                    
                    processed_count += 1
                
            except Exception as e:
                print(f"✗ Error processing message: {e}")
        
        print(f"\n✅ Processed {processed_count} reviews with sentiment analysis!")
        
        return processed_count
    
    def close(self):
        """Close connections"""
        
        self.redis_client.close()
        self.pg_client.close()
        
        print("✓ Connections closed")


def main():
    """Main function"""
    
    enricher = LLMSentimentEnricher()
    
    # Process stream (all messages)
    enricher.process_stream(count=40)
    
    # Close connections
    enricher.close()


if __name__ == "__main__":
    main()