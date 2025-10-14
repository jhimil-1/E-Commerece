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
    chatbot = ChatbotManager()
    
    # Create a session
    from auth import create_new_session
    session_id = await create_new_session("test_user")
    
    # Test various queries
    test_queries = [
        "dress",
        "business professional dress", 
        "smart thermostat",
        "streaming webcam",
        "clothing",
        "electronics"
    ]
    
    # Get user_id from session for testing
    user_id = chatbot._get_user_from_session(session_id)
    print(f"\n--- Session user_id: {user_id} ---")
    
    for query in test_queries:
        print(f"\n--- Testing query: '{query}' ---")
        response = await chatbot.handle_text_query(
            session_id=session_id,
            query=query
        )
        
        print(f"Response type: {type(response)}")
        if hasattr(response, 'products'):
            print(f"Products found: {len(response.products)}")
            for i, product in enumerate(response.products[:3]):
                print(f"  {i+1}. {product.get('name', 'Unknown')} - ${product.get('price', 'N/A')}")
        else:
            print(f"Response: {response}")
    
    # Test Qdrant search directly (no user filter)
    print(f"\n--- Direct Qdrant search (no user filter) ---")
    qdrant_results = qdrant_manager.search_similar_products(
        query_embedding=[0.1] * 512,  # dummy vector
        limit=5
    )
    print(f"Qdrant results: {len(qdrant_results)}")
    for i, product in enumerate(qdrant_results):
        print(f"  {i+1}. {product.get('name', 'Unknown')} - ${product.get('price', 'N/A')} (created_by: {product.get('created_by', 'N/A')})")
    
    # Test Qdrant search with user filter
    print(f"\n--- Direct Qdrant search (with user filter: {user_id}) ---")
    qdrant_results_with_user = qdrant_manager.search_similar_products(
        query_embedding=[0.1] * 512,  # dummy vector
        user_id=user_id,
        limit=5
    )
    print(f"Qdrant results with user filter: {len(qdrant_results_with_user)}")
    for i, product in enumerate(qdrant_results_with_user):
        print(f"  {i+1}. {product.get('name', 'Unknown')} - ${product.get('price', 'N/A')} (created_by: {product.get('created_by', 'N/A')})")

if __name__ == "__main__":
    asyncio.run(debug_search())