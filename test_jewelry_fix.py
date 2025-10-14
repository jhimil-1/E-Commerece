#!/usr/bin/env python3
"""Test script to verify jewelry search fix"""

import asyncio
import sys
import os
import uuid
from datetime import datetime

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from chatbot import ChatbotManager
from database import MongoDB

async def test_jewelry_search():
    """Test jewelry search to see if products are returned"""
    
    # Initialize chatbot manager
    chatbot_manager = ChatbotManager()
    
    # Create a test session
    db = MongoDB.get_db()
    session_id = str(uuid.uuid4())
    db.sessions.insert_one({
        'session_id': session_id,
        'user_id': 'test_user',
        'created_at': datetime.utcnow(),
        'last_activity': datetime.utcnow()
    })
    
    print("=== Testing Jewelry Search ===")
    response = await chatbot_manager.handle_text_query(session_id, "show jewelry")
    print(f"Query: show jewelry")
    print(f"Products found: {len(response.products)}")
    print(f"Response: {response.response}")
    
    if response.products:
        print("\nFirst 5 products:")
        for i, product in enumerate(response.products[:5]):
            print(f"  {i+1}. {product.get('name', 'Unknown')} - {product.get('category', 'Unknown')}")
            print(f"     Score: {product.get('similarity_score', 0):.3f}")
    
    print("\n=== Testing Jewellery Search (alternative spelling) ===")
    response2 = await chatbot_manager.handle_text_query(session_id, "show jewellery")
    print(f"Query: show jewellery")
    print(f"Products found: {len(response2.products)}")
    print(f"Response: {response2.response}")

if __name__ == "__main__":
    asyncio.run(test_jewelry_search())