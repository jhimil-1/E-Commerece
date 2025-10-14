#!/usr/bin/env python3

import sys
import asyncio
sys.path.append('.')

from chatbot import ChatbotManager
from auth import create_new_session
from database import MongoDB
import json

async def test_specific_queries():
    """Test the specific queries mentioned in the user conversation"""
    
    # Initialize chatbot manager
    chatbot_manager = ChatbotManager()
    
    # Create a proper session
    user_id = "test_user_123"
    session_id = await create_new_session(user_id)
    print(f"Created session: {session_id}")
    
    # Test the exact queries from the conversation
    test_queries = [
        "show me watch",
        "smartwatches", 
        "show me clothes",
        "show me jewellery",
        "men's watch",
        "show me similar product"  # This should trigger similar product logic
    ]
    
    print("Testing specific queries from the user conversation...")
    print("=" * 60)
    
    for query in test_queries:
        print(f"\nTesting query: '{query}'")
        print("-" * 40)
        
        try:
            # Process the query
            response = await chatbot_manager.handle_text_query(session_id, query)
            print(f"Response: {response.response}")
            print(f"Products found: {len(response.products)}")
            if response.products:
                for i, product in enumerate(response.products[:3], 1):
                    print(f"  {i}. {product.get('name', 'Unknown')} - ${product.get('price', 'N/A')}")
                 
        except Exception as e:
            print(f"ERROR: {str(e)}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("Test completed!")

if __name__ == "__main__":
    asyncio.run(test_specific_queries())