#!/usr/bin/env python3
"""
Final test of the chatbot with various user queries
"""

import asyncio
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from auth import create_new_session
from chatbot import ChatbotManager
# No need to import get_db for this test

async def test_chatbot():
    """Test the chatbot with various queries"""
    
    # Create a session
    print("Creating session...")
    session_id = await create_new_session("test_user_123")
    user_id = "test_user_123"
    print(f"Created session: {session_id} for user: {user_id}")
    
    # Initialize chatbot
    print("Initializing chatbot...")
    chatbot_manager = ChatbotManager()
    
    # Test queries
    test_queries = [
        "show me men's watch",
        "show me similar products",
        "show me jewelry",
        "show me smartwatches",
        "show me clothes",
        "show me women's dress"
    ]
    
    print("\n" + "="*60)
    print("TESTING VARIOUS QUERIES")
    print("="*60)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\nTest {i}: {query}")
        print("-" * 40)
        
        try:
            response = await chatbot_manager.handle_text_query(session_id, query)
            print(f"Response: {response['response']}")
            
            if response.get('products'):
                print(f"Products found: {len(response['products'])}")
                for j, product in enumerate(response['products'][:3], 1):
                    print(f"  {j}. {product['name']} - ${product['price']}")
            else:
                print("No products found")
                
        except Exception as e:
            print(f"Error: {e}")
    
    print("\n" + "="*60)
    print("TEST COMPLETED!")
    print("="*60)

if __name__ == "__main__":
    asyncio.run(test_chatbot())