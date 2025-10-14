#!/usr/bin/env python3
"""
Debug script to understand why category filtering isn't working in chatbot
"""

import asyncio
import logging
from database import MongoDB
from auth import create_new_session
from chatbot import ChatbotManager
from product_handler import ProductHandler
from qdrant_utils import QdrantManager
from clip_utils import clip_manager

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

async def debug_chatbot_filtering():
    """Debug category filtering in chatbot"""
    
    # Initialize components
    db = MongoDB.get_db()
    chatbot_manager = ChatbotManager()
    product_handler = ProductHandler()
    qdrant_manager = QdrantManager()
    
    # Create test session
    test_user_id = "test_user_123"
    session_id = await create_new_session(test_user_id)
    logger.info(f"Created test session: {session_id}")
    
    # Test query
    query = "show me clothing"
    category = "clothing"
    
    logger.info(f"\n{'='*60}")
    logger.info(f"Testing query: '{query}' with category: '{category}'")
    logger.info(f"{'='*60}")
    
    # Test direct product handler search
    logger.info("\n1. Testing Direct Product Handler Search:")
    try:
        # Generate embedding for the query
        query_embedding = clip_manager.get_text_embedding(query)
        
        search_result = await product_handler.search_products(
            query=query,
            query_embedding=query_embedding,
            user_id=test_user_id,
            category=category,
            limit=10
        )
        
        if search_result['status'] == 'success':
            products = search_result['results']
            logger.info(f"Product handler returned {len(products)} products:")
            categories_found = set()
            for i, product in enumerate(products, 1):
                product_category = product.get('category', 'unknown')
                categories_found.add(product_category.lower())
                logger.info(f"  {i}. {product.get('name', 'Unknown')} - Category: {product_category}")
            
            logger.info(f"Categories found: {categories_found}")
            if len(categories_found) == 1 and category.lower() in categories_found:
                logger.info("✅ Product handler category filtering: PASSED")
            else:
                logger.info("❌ Product handler category filtering: FAILED")
        else:
            logger.error(f"Product handler search failed: {search_result['message']}")
            
    except Exception as e:
        logger.error(f"Product handler search failed: {e}")
    
    # Test chatbot search
    logger.info("\n2. Testing Chatbot Search:")
    try:
        chatbot_response = await chatbot_manager.handle_text_query(
            session_id=session_id,
            query=query,
            category=category,
            limit=10
        )
        
        logger.info(f"Chatbot returned {len(chatbot_response.products)} products:")
        categories_found = set()
        for i, product in enumerate(chatbot_response.products, 1):
            product_category = product.get('category', 'unknown')
            categories_found.add(product_category.lower())
            logger.info(f"  {i}. {product.get('name', 'Unknown')} - Category: {product_category}")
        
        logger.info(f"Categories found: {categories_found}")
        if len(categories_found) == 1 and category.lower() in categories_found:
            logger.info("✅ Chatbot category filtering: PASSED")
        else:
            logger.info("❌ Chatbot category filtering: FAILED")
            
    except Exception as e:
        logger.error(f"Chatbot search failed: {e}")

if __name__ == "__main__":
    asyncio.run(debug_chatbot_filtering())