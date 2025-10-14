#!/usr/bin/env python3
"""
Script to inspect what products are actually stored in Qdrant
"""

import asyncio
from qdrant_utils import qdrant_manager
from clip_utils import clip_manager
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def inspect_qdrant_products():
    """Inspect products stored in Qdrant"""
    
    # Generate a simple query to get some results
    query = "dress"
    query_embedding = clip_manager.get_text_embedding(query)
    
    # Search without any filters to see what's available
    logger.info("=== Searching Qdrant without filters ===")
    results = qdrant_manager.search_similar_products(
        query_embedding=query_embedding,
        user_id=None,
        category_filter=None,
        limit=10
    )
    
    logger.info(f"Found {len(results)} products without filters")
    
    for i, result in enumerate(results):
        logger.info(f"\nProduct {i+1}:")
        logger.info(f"  ID: {result.get('id')}")
        logger.info(f"  Name: {result.get('name')}")
        logger.info(f"  Category: {result.get('category')}")
        logger.info(f"  Score: {result.get('score')}")
        logger.info(f"  Payload keys: {list(result.get('payload', {}).keys())}")
        
        # Check if created_by exists in payload
        payload = result.get('payload', {})
        if 'created_by' in payload:
            logger.info(f"  Created by: {payload['created_by']}")
        else:
            logger.info("  Created by: NOT FOUND in payload")
    
    # Now test with user filter
    logger.info("\n=== Testing with user filter ===")
    filtered_results = qdrant_manager.search_similar_products(
        query_embedding=query_embedding,
        user_id="test_user",
        category_filter=None,
        limit=10
    )
    
    logger.info(f"Found {len(filtered_results)} products with user filter 'test_user'")

if __name__ == "__main__":
    asyncio.run(inspect_qdrant_products())