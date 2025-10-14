#!/usr/bin/env python3
"""
Analyze available categories and search filtering
"""

import asyncio
from database import MongoDB
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def analyze_categories():
    """Analyze categories and search behavior"""
    
    # Get database connection
    db = MongoDB.get_db()
    if db is None:
        logger.error("Failed to connect to database")
        return
    
    # Check what categories exist
    logger.info("=== Available Categories ===")
    categories = db.products.distinct("category")
    logger.info(f"Found categories: {categories}")
    
    # Check category distribution
    logger.info("\n=== Category Distribution ===")
    for category in categories:
        count = db.products.count_documents({"category": category})
        logger.info(f"{category}: {count} products")
    
    # Check if products have proper category field for Qdrant
    logger.info("\n=== Qdrant Category Check ===")
    from qdrant_utils import qdrant_manager
    
    # Get a few sample products from Qdrant
    try:
        # Search without category filter to see what we get
        from clip_utils import clip_manager
        query_embedding = clip_manager.get_text_embedding("clothing")
        
        results = qdrant_manager.search_similar_products(
            query_embedding=query_embedding,
            user_id=None,  # No user filter
            limit=10
        )
        
        logger.info(f"Sample Qdrant results for 'clothing' query:")
        for i, result in enumerate(results[:5]):
            payload = result.get('payload', {})
            logger.info(f"  {i+1}. {payload.get('name', 'Unknown')} - Category: {payload.get('category', 'Missing')}")
            
    except Exception as e:
        logger.error(f"Failed to search Qdrant: {e}")

if __name__ == "__main__":
    asyncio.run(analyze_categories())