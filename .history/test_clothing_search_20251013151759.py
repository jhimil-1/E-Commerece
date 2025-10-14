#!/usr/bin/env python3
"""
Test script to debug clothing search issues
"""

import asyncio
import json
from qdrant_utils import qdrant_manager
from chatbot import ChatbotManager
from clip_utils import clip_manager
from auth import create_new_session
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_clothing_search():
    """Test clothing search with different queries"""
    
    # Create a test session using actual user_id UUID
    test_user_id = "9ba7d438-2066-4466-991d-e4f78e728a78"  # test_user_02ff81cd
    session_id = await create_new_session(test_user_id)
    logger.info(f"Created test session: {session_id}")
    
    # Test different clothing-related queries
    test_queries = ["chlothes", "clothes", "dress", "clothing", "apparel"]
    
    chatbot_manager = ChatbotManager()
    
    for query in test_queries:
        logger.info(f"\n=== Testing query: '{query}' ===")
        
        # Test chatbot search
        try:
            chatbot_results = await chatbot_manager.handle_text_query(
                session_id=session_id,
                query=query,
                limit=10  # Increase limit to see more results
            )
            
            logger.info(f"Chatbot results for '{query}': {len(chatbot_results.products)} products")
            
            # Show all results with their categories
            for i, product in enumerate(chatbot_results.products):
                logger.info(f"  {i+1}. {product['name']} - ${product['price']} - Category: {product.get('category', 'Unknown')}")
                
        except Exception as e:
            logger.error(f"Chatbot search failed for '{query}': {e}")
        
        # Also test direct Qdrant search to see what embeddings find
        try:
            query_embedding = clip_manager.get_text_embedding(query)
            qdrant_results = qdrant_manager.search_similar_products(
                query_embedding=query_embedding,
                user_id=test_user_id,
                limit=10
            )
            
            logger.info(f"Qdrant results for '{query}': {len(qdrant_results)} products")
            for i, result in enumerate(qdrant_results[:3]):  # Show top 3
                payload = result.get('payload', {})
                logger.info(f"  {i+1}. {payload.get('name', 'Unknown')} - Category: {payload.get('category', 'Unknown')}")
                
        except Exception as e:
            logger.error(f"Qdrant search failed for '{query}': {e}")

if __name__ == "__main__":
    asyncio.run(test_clothing_search())