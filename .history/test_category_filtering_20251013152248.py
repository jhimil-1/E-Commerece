#!/usr/bin/env python3
"""
Test category filtering to debug the clothing search issue
"""

import asyncio
from qdrant_utils import qdrant_manager
from clip_utils import clip_manager
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_category_filtering():
    """Test category filtering with different case variations"""
    
    # Test different category filters
    test_categories = ["clothing", "Clothing", "CLOTHING", "dress", "electronics"]
    test_query = "clothes"
    
    # Generate query embedding
    query_embedding = clip_manager.get_text_embedding(test_query)
    
    for category in test_categories:
        logger.info(f"\n=== Testing category filter: '{category}' ===")
        
        try:
            # Test with category filter
            results = qdrant_manager.search_similar_products(
                query_embedding=query_embedding,
                user_id=None,  # No user filter for this test
                category_filter=category,
                limit=10
            )
            
            logger.info(f"Found {len(results)} results with category filter '{category}'")
            
            # Show categories of results
            category_counts = {}
            for result in results:
                cat = result.get('payload', {}).get('category', 'Unknown')
                category_counts[cat] = category_counts.get(cat, 0) + 1
            
            logger.info(f"Category distribution: {category_counts}")
            
            # Show first few results
            for i, result in enumerate(results[:3]):
                payload = result.get('payload', {})
                logger.info(f"  {i+1}. {payload.get('name', 'Unknown')} - Category: {payload.get('category', 'Unknown')}")
                
        except Exception as e:
            logger.error(f"Category filter test failed for '{category}': {e}")
    
    # Test without category filter for comparison
    logger.info(f"\n=== Testing without category filter ===")
    try:
        results_no_filter = qdrant_manager.search_similar_products(
            query_embedding=query_embedding,
            user_id=None,
            category_filter=None,
            limit=10
        )
        
        logger.info(f"Found {len(results_no_filter)} results without category filter")
        
        # Show categories of results
        category_counts = {}
        for result in results_no_filter:
            cat = result.get('payload', {}).get('category', 'Unknown')
            category_counts[cat] = category_counts.get(cat, 0) + 1
        
        logger.info(f"Category distribution: {category_counts}")
        
    except Exception as e:
        logger.error(f"No filter test failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_category_filtering())