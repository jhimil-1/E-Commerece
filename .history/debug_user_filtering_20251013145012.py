#!/usr/bin/env python3
"""
Debug script to test user filtering in Qdrant search
"""

import asyncio
import json
from qdrant_utils import qdrant_manager
from chatbot_manager import chatbot_manager
from auth import create_new_session
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_user_filtering():
    """Test user filtering in Qdrant search"""
    
    # Create a test session
    session_id = await create_new_session("test_user")
    logger.info(f"Created test session: {session_id}")
    
    # Test queries
    test_queries = ["dress", "electronics", "jewelry"]
    
    for query in test_queries:
        logger.info(f"\n=== Testing query: '{query}' ===")
        
        # Test chatbot search (with user filtering)
        try:
            chatbot_results = await chatbot_manager.handle_text_query(
                session_id=session_id,
                query=query,
                limit=5
            )
            logger.info(f"Chatbot results for '{query}': {len(chatbot_results.products)} products")
            if chatbot_results.products:
                logger.info(f"First result: {chatbot_results.products[0]['name']}")
        except Exception as e:
            logger.error(f"Chatbot search failed for '{query}': {e}")
        
        # Test direct Qdrant search without user filtering
        try:
            # Generate query embedding using CLIP
            from clip_manager import clip_manager
            query_embedding = clip_manager.get_text_embedding(query)
            
            qdrant_results = qdrant_manager.search_similar_products(
                query_embedding=query_embedding,
                user_id=None,  # No user filtering
                limit=5
            )
            logger.info(f"Qdrant results (no user filter) for '{query}': {len(qdrant_results)} products")
            if qdrant_results:
                logger.info(f"First result: {qdrant_results[0]['name']}")
                logger.info(f"Payload keys: {list(qdrant_results[0].get('payload', {}).keys())}")
        except Exception as e:
            logger.error(f"Qdrant search failed for '{query}': {e}")
        
        # Test direct Qdrant search with user filtering
        try:
            qdrant_results_filtered = qdrant_manager.search_similar_products(
                query_embedding=query_embedding,
                user_id="test_user",  # With user filtering
                limit=5
            )
            logger.info(f"Qdrant results (with user filter) for '{query}': {len(qdrant_results_filtered)} products")
            if qdrant_results_filtered:
                logger.info(f"First result: {qdrant_results_filtered[0]['name']}")
        except Exception as e:
            logger.error(f"Qdrant filtered search failed for '{query}': {e}")

if __name__ == "__main__":
    asyncio.run(test_user_filtering())