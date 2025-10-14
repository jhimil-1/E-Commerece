#!/usr/bin/env python3
"""
Test script to verify jewelry search behavior and category filtering
"""

import asyncio
import logging
from uuid import UUID
from chatbot import ChatbotManager
from database import get_database
from qdrant_utils import QdrantManager
from config import settings

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s:%(message)s')
logger = logging.getLogger(__name__)

async def test_jewelry_search():
    """Test jewelry search with various queries"""
    
    # Test user ID
    test_user_id = UUID("9ba7d438-2066-4466-991d-e4f78e728a78")
    
    # Initialize components
    db = get_database()
    chatbot = ChatbotManager()
    qdrant_manager = QdrantManager()
    
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
                session_id="test-session-jewelry",
                user_id=test_user_id,
                query=query
            )
            
            if chatbot_response.get("products"):
                logger.info(f"Found {len(chatbot_response['products'])} products:")
                for i, product in enumerate(chatbot_response["products"], 1):
                    category = product.get("category", "Unknown")
                    logger.info(f"  {i}. {product['name']} - ${product['price']} - Category: {category}")
            else:
                logger.info("No products found")
                
        except Exception as e:
            logger.error(f"Chatbot search failed: {e}")
        
        # Test direct Qdrant search with category filter
        try:
            logger.info("\nDirect Qdrant search with 'jewelry' category:")
            qdrant_results = qdrant_manager.search_similar_products(
                query=query,
                user_id=test_user_id,
                category="jewelry",
                limit=10
            )
            
            if qdrant_results:
                logger.info(f"Found {len(qdrant_results)} products:")
                for i, result in enumerate(qdrant_results, 1):
                    payload = result.payload
                    category = payload.get("category", "Unknown")
                    logger.info(f"  {i}. {payload['name']} - Category: {category}")
            else:
                logger.info("No products found")
                
        except Exception as e:
            logger.error(f"Qdrant search failed: {e}")
            
        logger.info("-" * 40)

if __name__ == "__main__":
    asyncio.run(test_jewelry_search())