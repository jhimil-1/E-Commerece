#!/usr/bin/env python3
"""
Debug script to check Qdrant search result format
"""

import sys
sys.path.append('.')

from database import MongoDB
from qdrant_utils import QdrantManager
import clip_utils
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def debug_qdrant_format():
    """Debug Qdrant search result format"""
    print("=== DEBUG QDRANT FORMAT ===")
    
    # Get database and Qdrant
    db = MongoDB.get_db()
    qdrant_manager = QdrantManager()
    
    # Test parameters
    user_id = "9ba7d438-2066-4466-991d-e4f78e728a78"
    query = "jacket"
    
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
            limit=5,
            min_score=0.0
        )
        print(f"Results type: {type(results)}")
        print(f"Results length: {len(results)}")
        if results:
            print(f"First result type: {type(results[0])}")
            print(f"First result: {results[0]}")
            
            # Check if it's a dict or object
            if isinstance(results[0], dict):
                print("Result is a dictionary")
                print(f"Keys: {list(results[0].keys())}")
            else:
                print("Result is an object")
                print(f"Attributes: {dir(results[0])}")
                
                # Try to access attributes
                try:
                    print(f"product_id: {getattr(results[0], 'product_id', 'not found')}")
                    print(f"score: {getattr(results[0], 'score', 'not found')}")
                    print(f"payload: {getattr(results[0], 'payload', 'not found')}")
                except Exception as e:
                    print(f"Error accessing attributes: {e}")
    except Exception as e:
        print(f"Error in Qdrant search: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_qdrant_format()