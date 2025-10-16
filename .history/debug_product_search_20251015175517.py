#!/usr/bin/env python3
"""
Debug script to understand product search issues
"""

import sys
sys.path.append('.')

from database import MongoDB
from qdrant_utils import QdrantManager
import clip_utils
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def debug_product_search():
    """Debug product search process"""
    print("=== DEBUG PRODUCT SEARCH ===")
    
    # Get database and Qdrant
    db = MongoDB.get_db()
    qdrant_manager = QdrantManager()
    
    # Test parameters
    user_id = "9ba7d438-2066-4466-991d-e4f78e728a78"
    query = "earrings"
    
    print(f"Testing search for user: {user_id}, query: {query}")
    
    # Generate embedding
    try:
        clip_manager = clip_utils.CLIPManager()
        query_embedding = clip_manager.get_text_embedding(query)
        print(f"Generated embedding with {len(query_embedding)} dimensions")
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return
    
    # Test Qdrant search directly
    print("\n1. Testing Qdrant search with user filter only...")
    try:
        results = qdrant_manager.search_similar_products(
            query_embedding=query_embedding,
            user_id=user_id,
            limit=10,
            min_score=0.0
        )
        print(f"Results with user filter: {len(results)}")
        if results:
            print(f"First result: {results[0]}")
    except Exception as e:
        print(f"Error in Qdrant search with user filter: {e}")
    
    print("\n2. Testing Qdrant search without any filters...")
    try:
        results = qdrant_manager.search_similar_products(
            query_embedding=query_embedding,
            limit=10,
            min_score=0.0
        )
        print(f"Results without filters: {len(results)}")
        if results:
            print(f"First result: {results[0]}")
    except Exception as e:
        print(f"Error in Qdrant search without filters: {e}")
    
    print("\n3. Testing Qdrant search with category filter...")
    try:
        results = qdrant_manager.search_similar_products(
            query_embedding=query_embedding,
            user_id=user_id,
            category_filter="Jewellery",
            limit=10,
            min_score=0.0
        )
        print(f"Results with category filter: {len(results)}")
        if results:
            print(f"First result: {results[0]}")
    except Exception as e:
        print(f"Error in Qdrant search with category filter: {e}")
    
    # Check what products exist for this user
    print("\n4. Checking products for this user...")
    try:
        products = list(db.products.find({"created_by": user_id}).limit(5))
        print(f"Found {len(products)} products for user {user_id}")
        for product in products:
            print(f"- {product.get('name')} (category: {product.get('category')})")
    except Exception as e:
        print(f"Error checking products: {e}")

if __name__ == "__main__":
    debug_product_search()