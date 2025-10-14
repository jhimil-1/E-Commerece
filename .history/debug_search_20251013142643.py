#!/usr/bin/env python3
"""
Debug script to test the search functionality and see what's happening
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from chatbot import ChatbotManager
from database import MongoDB
from qdrant_utils import qdrant_manager
from clip_utils import clip_manager

async def debug_search():
    """Debug the search functionality"""
    
    print("=== INITIALIZING CHATBOT ===")
    chatbot = JewelleryChatbot()
    
    # Create a test session
    print("\n=== CREATING TEST SESSION ===")
    session_result = chatbot.create_chat_session("test_user_123")
    session_id = session_result['session_id']
    print(f"Created session: {session_id}")
    
    # Test different queries
    test_queries = [
        "dress",
        "show me dresses", 
        "clothing",
        "jewelry",
        "ring"
    ]
    
    for query in test_queries:
        print(f"\n=== TESTING QUERY: '{query}' ===")
        
        try:
            # Get query embedding
            print("Getting query embedding...")
            query_embedding = clip_manager.get_text_embedding(query)
            print(f"Embedding shape: {len(query_embedding)}")
            
            # Search in Qdrant
            print("Searching Qdrant...")
            products = qdrant_manager.search_similar_products(
                query_embedding=query_embedding,
                user_id="test_user_123",
                category_filter=None,  # No category filter
                limit=10
            )
            
            print(f"Found {len(products)} products")
            
            if products:
                for i, product in enumerate(products[:3]):
                    print(f"  {i+1}. {product.get('name', 'Unknown')} - ${product.get('price', 'N/A')} ({product.get('category', 'N/A')})")
                    print(f"     Score: {product.get('score', 'N/A')}")
                    print(f"     ID: {product.get('product_id', 'N/A')}")
            else:
                print("  No products found!")
                
            # Test with chatbot
            print("Testing with chatbot...")
            response = await chatbot.handle_text_query(session_id, query)
            print(f"Response: {response.response[:200]}...")
            
            if response.products:
                print(f"Products in response: {len(response.products)}")
                for p in response.products[:2]:
                    print(f"  - {p.get('name', 'Unknown')}")
            else:
                print("No products in response")
                
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_search())