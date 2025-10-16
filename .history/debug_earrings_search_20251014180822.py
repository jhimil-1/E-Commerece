#!/usr/bin/env python3
"""
Debug script to understand why earring searches aren't returning jewelry products
"""

import asyncio
import logging
from database import MongoDB
from auth import create_new_session
from chatbot import ChatbotManager
from product_handler import ProductHandler
from qdrant_utils import QdrantManager

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

async def debug_earrings_search():
    """Debug earring searches"""
    
    # Initialize components
    db = MongoDB.get_db()
    chatbot_manager = ChatbotManager()
    product_handler = ProductHandler()
    qdrant_manager = QdrantManager()
    
    # Create test session
    test_user_id = "test_user_123"
    session_id = await create_new_session(test_user_id)
    logger.info(f"Created test session: {session_id}")
    
    # Test queries for earrings
    test_queries = [
        "show me earrings",
        "earrings", 
        "gold earrings",
        "diamond earrings"
    ]
    
    for query in test_queries:
        logger.info(f"\n{'='*60}")
        logger.info(f"Testing query: '{query}'")
        logger.info(f"{'='*60}")
        
        # Test direct product handler search
        logger.info(f"\n1. Testing Direct Product Handler Search for '{query}':")
        try:
            search_result = await product_handler.search_products(
                query=query,
                user_id=test_user_id,
                category=None,  # Let it auto-detect
                limit=10
            )
            
            if search_result['status'] == 'success':
                products = search_result['results']
                logger.info(f"Product handler returned {len(products)} products:")
                categories_found = set()
                jewelry_count = 0
                
                for i, product in enumerate(products, 1):
                    product_category = product.get('category', 'unknown')
                    categories_found.add(product_category.lower())
                    if 'jewelry' in product_category.lower():
                        jewelry_count += 1
                    logger.info(f"  {i}. {product.get('name', 'Unknown')} - Category: {product_category}")
                
                logger.info(f"Categories found: {categories_found}")
                logger.info(f"Jewelry products: {jewelry_count}/{len(products)}")
                
                if jewelry_count > 0:
                    logger.info("✅ Product handler found jewelry products")
                else:
                    logger.info("❌ Product handler found NO jewelry products")
            else:
                logger.error(f"Product handler search failed: {search_result['message']}")
                
        except Exception as e:
            logger.error(f"Product handler search failed: {e}")
            logger.exception(e)
        
        # Test chatbot search
        logger.info(f"\n2. Testing Chatbot Search for '{query}':")
        try:
            logger.info("Calling chatbot_manager.handle_text_query...")
            chatbot_response = await chatbot_manager.handle_text_query(
                session_id=session_id,
                query=query,
                category=None,  # Let it auto-detect
                limit=10
            )
            
            logger.info(f"Chatbot returned {len(chatbot_response.products)} products:")
            if chatbot_response.products:
                categories_found = set()
                jewelry_count = 0
                
                for i, product in enumerate(chatbot_response.products, 1):
                    product_category = product.get('category', 'unknown')
                    categories_found.add(product_category.lower())
                    if 'jewelry' in product_category.lower():
                        jewelry_count += 1
                    logger.info(f"  {i}. {product.get('name', 'Unknown')} - Category: {product_category}")
                
                logger.info(f"Categories found: {categories_found}")
                logger.info(f"Jewelry products: {jewelry_count}/{len(chatbot_response.products)}")
                
                if jewelry_count > 0:
                    logger.info("✅ Chatbot found jewelry products")
                else:
                    logger.info("❌ Chatbot found NO jewelry products")
            else:
                logger.info("No products returned by chatbot")
                logger.info(f"Chatbot response text: {chatbot_response.response}")
                
        except Exception as e:
            logger.error(f"Chatbot search failed: {e}")
            logger.exception(e)

if __name__ == "__main__":
    asyncio.run(debug_earrings_search())