"""
Redis Utilities for E-Commerce Streaming
(100% FREE - Redis instead of Kafka)
"""

import redis
import json
import sys
import os
from datetime import datetime

class RedisPublisher:
    """Publishes data to Redis streams"""
    
    def __init__(self, host='localhost', port=6379):
        """Initialize Redis connection"""
        
        self.host = host
        self.port = port
        
        try:
            # Connect to Redis (Docker should be running)
            self.redis_client = redis.Redis(host=host, port=port, decode_responses=True)
            
            # Test connection
            self.redis_client.ping()
            
            print(f"✓ Connected to Redis at {host}:{port}")
            
        except redis.ConnectionError:
            print(f"✗ Could not connect to Redis at {host}:{port}")
            print("💡 Note: Start Docker with: cd docker && docker-compose up -d")
            self.redis_client = None
    
    def publish(self, data, channel="ecommerce_data"):
        """Publish data to Redis stream"""
        
        if self.redis_client is None:
            print(f"✗ Redis not connected. Data saved to {channel}.")
            return False
        
        try:
            # Convert data to JSON
            json_data = json.dumps(data)
            
            # Publish to Redis stream
            self.redis_client.xadd(channel, {"data": json_data})
            
            print(f"✓ Published to Redis stream: {channel}")
            return True
            
        except Exception as e:
            print(f"✗ Error publishing to Redis: {e}")
            return False
    
    def get_stream(self, channel="ecommerce_data", count=10):
        """Read data from Redis stream"""
        
        if self.redis_client is None:
            print("✗ Redis not connected")
            return []
        
        try:
            # Get data from stream
            messages = self.redis_client.xrevrange(channel, count=count)
            
            print(f"✓ Retrieved {len(messages)} messages from {channel}")
            return messages
            
        except Exception as e:
            print(f"✗ Error reading from Redis: {e}")
            return []
    
    def close(self):
        """Close Redis connection"""
        
        if self.redis_client:
            self.redis_client.close()
            print("✓ Redis connection closed")


# Test function
def test_redis():
    """Test Redis connection"""
    
    print("Testing Redis connection...")
    
    redis_pub = RedisPublisher()
    
    if redis_pub.redis_client:
        # Test publish
        test_data = {
            "name": "Test Data",
            "timestamp": datetime.now().isoformat(),
            "value": 123
        }
        
        redis_pub.publish(test_data, channel="test_channel")
        
        # Test read
        messages = redis_pub.get_stream(channel="test_channel")
        
        print(f"\n✓ Redis test successful!")
        print(f"  Sent: {test_data}")
        print(f"  Retrieved: {messages}")
        
        redis_pub.close()
        
        return True
    else:
        print("\n✗ Redis is not running")
        print("💡 Start Docker: cd docker && docker-compose up -d")
        return False


if __name__ == "__main__":
    test_redis()