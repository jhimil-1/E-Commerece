#!/usr/bin/env python3
"""
Test script to verify jewelry search behavior and category filtering
"""

import asyncio
import logging
from uuid import UUID
from chatbot import ChatbotManager
from database import MongoDB
from qdrant_utils import QdrantManager
from clip_utils import clip_manager
from auth import create_new_session

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s:%(message)s')
logger = logging.getLogger(__name__)

async def test_jewelry_search():
    """Test jewelry search with various queries"""
    
    # Test user ID
    test_user_id = UUID("9ba7d438-2066-4466-991d-e4f78e728a78")
    
    # Initialize components
    db = MongoDB.get_db()
    chatbot = ChatbotManager()
    qdrant_manager = QdrantManager()
    
    # Create a test session
    session_id = await create_new_session(str(test_user_id))
    logger.info(f"Created test session: {session_id}")
    
    # Test jewelry-related queries
    jewelry_queries = [
        "jewelry",
        "jewellery", 
        "show me jewelry",
        "earrings",
        "necklace",
        "bracelet",
        "ring",
        "watch"
    ]
    
    logger.info(f"Testing jewelry searches for user: {test_user_id}")
    logger.info("=" * 60)
    
    for query in jewelry_queries:
        logger.info(f"\n🔍 Testing query: '{query}'")
        logger.info("-" * 40)
        
        # Test chatbot search
        try:
            logger.info("Chatbot search:")
            chatbot_response = await chatbot.handle_text_query(
                session_id=session_id,
                query=query
            )
            
            if chatbot_response.products:
                logger.info(f"Found {len(chatbot_response.products)} products:")
                for i, product in enumerate(chatbot_response.products, 1):
                    category = product.get("category", "Unknown")
                    logger.info(f"  {i}. {product['name']} - ${product['price']} - Category: {category}")
            else:
                logger.info("No products found")
                
        except Exception as e:
            logger.error(f"Chatbot search failed: {e}")
        
        # Test direct Qdrant search with category filter
        try:
            logger.info("\nDirect Qdrant search with 'jewelry' category:")
            # Generate query embedding first
            query_embedding = clip_manager.get_text_embedding(query)
            logger.info(f"Generated embedding for '{query}' with shape: {len(query_embedding)}")
            
            qdrant_results = qdrant_manager.search_similar_products(
                query_embedding=query_embedding,
                user_id=test_user_id,
                category_filter="jewelry",
                limit=10
            )
            
            if qdrant_results:
                logger.info(f"Found {len(qdrant_results)} products:")
                for i, result in enumerate(qdrant_results, 1):
                    category = result.get("category", "Unknown")
                    logger.info(f"  {i}. {result['name']} - Category: {category}")
            else:
                logger.info("No products found")
                
        except Exception as e:
            logger.error(f"Qdrant search failed: {e}")
            
        logger.info("-" * 40)

if __name__ == "__main__":
    asyncio.run(test_jewelry_search())