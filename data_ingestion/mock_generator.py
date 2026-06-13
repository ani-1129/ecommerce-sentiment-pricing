"""
Mock E-Commerce Data Generator
Generates fake reviews and orders → publishes to Redis ✓ FIXED
"""

import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta
import json
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.redis_utils import RedisPublisher

# Initialize Faker
fake = Faker()
fake.locale = 'en_US'

class MockDataGenerator:
    """Generates synthetic e-commerce data"""
    
    def __init__(self):
        self.products = [
            "Wireless Bluetooth Headphones", "Smartphone Charger 20W",
            "Laptop Stand Aluminum", "Gaming Mouse RGB",
            "USB-C Cable 2m", "Portable SSD 1TB",
            "Mechanical Keyboard", "Webcam 1080p",
            "Power Bank 20000mAh", "Smart Watch Fitness"
        ]
        self.categories = ["Electronics", "Accessories", "Gaming", "Computers"]
        self.statuses = ["Delivered", "Shipped", "Processing", "Cancelled"]
    
    def generate_review(self, order_id=None):
        """Generate a single product review"""
        
        review = {
            "review_id": fake.uuid4(),
            "order_id": order_id or fake.uuid4(),
            "product_name": random.choice(self.products),
            "category": random.choice(self.categories),
            "rating": random.randint(1, 5),
            "review_text": fake.paragraph(nb_sentences=3),
            "review_date": datetime.now() - timedelta(days=random.randint(1, 30)),
            "verified_purchase": random.choice([True, False])
        }
        
        # Convert datetime to string for JSON serialization ✓
        review['review_date'] = review['review_date'].isoformat()
        
        return review
    
    def generate_order(self):
        """Generate a single order"""
        
        order = {
            "order_id": fake.uuid4(),
            "customer_id": fake.uuid4(),
            "product_name": random.choice(self.products),
            "category": random.choice(self.categories),
            "price": round(random.uniform(20, 200), 2),
            "quantity": random.randint(1, 5),
            "order_status": random.choice(self.statuses),
            "order_date": datetime.now() - timedelta(days=random.randint(1, 30)),
            "shipping_city": fake.city()
        }
        
        # Convert datetime to string for JSON serialization ✓
        order['order_date'] = order['order_date'].isoformat()
        
        return order
    
    def generate_batch(self, n=10):
        """Generate multiple reviews and orders"""
        
        print(f"🚀 Generating {n} reviews and orders...")
        
        records = []
        
        for i in range(n):
            # Generate order
            order = self.generate_order()
            records.append(order)
            
            # Generate review linked to order
            review = self.generate_review(order['order_id'])
            records.append(review)
        
        print(f"✅ Generated {len(records)} total records")
        return records
    
    def save_to_csv(self, records, filename="mock_data.csv"):
        """Save records to CSV file"""
        
        df = pd.DataFrame(records)
        df.to_csv(filename, index=False)
        print(f"✅ Saved {len(records)} records to {filename}")
        return df

def main():
    """Main function to generate and publish data"""
    
    generator = MockDataGenerator()
    
    # Generate batch of data
    records = generator.generate_batch(n=10)
    
    # Save to CSV
    generator.save_to_csv(records)
    
    # Publish to Redis
    try:
        redis_pub = RedisPublisher()
        
        for record in records:
            # Remove any None values before publishing
            clean_record = {k: v for k, v in record.items() if v is not None}
            
            # Publish to Redis ✓
            redis_pub.publish(clean_record, channel="ecommerce_data")
            
            print(f"✓ Published: {clean_record['order_id'] or clean_record['review_id']}")
        
        print(f"✅ Batch complete! Total: {len(records)} records")
        
    except Exception as e:
        print(f"✗ Error publishing to Redis: {e}")
        print("💡 Note: Redis might not be running. Data saved to CSV anyway.")

if __name__ == "__main__":
    main()