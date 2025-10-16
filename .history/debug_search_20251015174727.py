import asyncio
import os
import sys
from datetime import datetime
from typing import Dict, Any, List

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from product_handler import ProductHandler
from database import get_database
from qdrant_utils import QdrantManager

async def debug_search():
    """Debug the search process step by step"""
    
    # Initialize components
    db = get_database()
    qdrant_manager = QdrantManager()
    product_handler = ProductHandler(db, qdrant_manager)
    
    user_id = "9ba7d438-2066-4466-991d-e4f78e728a78"
    query = "earrings"
    
    print(f"=== DEBUG SEARCH STARTED ===")
    print(f"Query: '{query}'")
    print(f"User ID: {user_id}")
    print(f"Time: {datetime.now()}")
    print()
    
    # Step 1: Check Qdrant directly
    print("1. Checking Qdrant directly...")
    try:
        # Get embeddings for the query
        from clip_utils import CLIPProcessor
        clip_processor = CLIPProcessor()
        text_embedding = clip_processor.get_text_embedding(query)
        
        if text_embedding is not None:
            print(f"   Text embedding generated: {len(text_embedding)} dimensions")
            
            # Search Qdrant without category filter
            qdrant_results_no_filter = qdrant_manager.search_similar(
                query_vector=text_embedding,
                user_id=user_id,
                category_filter=None,
                limit=20
            )
            print(f"   Qdrant results (no category filter): {len(qdrant_results_no_filter)}")
            
            # Search Qdrant with jewelry category
            qdrant_results_jewelry = qdrant_manager.search_similar(
                query_vector=text_embedding,
                user_id=user_id,
                category_filter="Jewellery",
                limit=20
            )
            print(f"   Qdrant results (Jewellery category): {len(qdrant_results_jewelry)}")
            
            # Search Qdrant with jewelry category (American spelling)
            qdrant_results_jewelry_us = qdrant_manager.search_similar(
                query_vector=text_embedding,
                user_id=user_id,
                category_filter="Jewelry",
                limit=20
            )
            print(f"   Qdrant results (Jewelry category): {len(qdrant_results_jewelry_us)}")
            
            # Print first few results from each search
            if qdrant_results_no_filter:
                print(f"   First result (no filter): {qdrant_results_no_filter[0].get('payload', {}).get('name', 'Unknown')}")
                print(f"   Score: {qdrant_results_no_filter[0].get('score', 0)}")
            
            if qdrant_results_jewelry:
                print(f"   First result (Jewellery): {qdrant_results_jewelry[0].get('payload', {}).get('name', 'Unknown')}")
                print(f"   Score: {qdrant_results_jewelry[0].get('score', 0)}")
                
        else:
            print("   ERROR: Could not generate text embedding")
            
    except Exception as e:
        print(f"   ERROR in Qdrant search: {str(e)}")
    
    print()
    
    # Step 2: Check user lookup
    print("2. Checking user lookup...")
    try:
        # Try to find the user in different ways
        user = db.users.find_one({"_id": user_id})
        if user:
            print(f"   User found by _id: {user.get('username', 'Unknown')}")
        else:
            print(f"   User not found by _id: {user_id}")
            
        user_by_username = db.users.find_one({"username": user_id})
        if user_by_username:
            print(f"   User found by username: {user_by_username.get('username', 'Unknown')}")
        else:
            print(f"   User not found by username: {user_id}")
            
    except Exception as e:
        print(f"   ERROR in user lookup: {str(e)}")
    
    print()
    
    # Step 3: Try the actual search
    print("3. Trying actual product search...")
    try:
        results = await product_handler.search_products(
            query=query,
            user_id=user_id,
            category=None,  # No category filter first
            min_score=0.0,
            limit=20
        )
        
        print(f"   Search results: {results.get('status', 'Unknown')}")
        print(f"   Products found: {len(results.get('results', []))}")
        
        if results.get('metadata'):
            metadata = results['metadata']
            print(f"   User lookup success: {metadata.get('user_lookup_success', 'Unknown')}")
            print(f"   Qdrant user ID: {metadata.get('qdrant_user_id', 'Unknown')}")
            print(f"   Products validated: {metadata.get('validation', {}).get('products_validated', 'Unknown')}")
            
        if results.get('results'):
            print(f"   First result: {results['results'][0].get('name', 'Unknown')}")
            print(f"   Relevance score: {results['results'][0].get('relevance_score', 0)}")
            
    except Exception as e:
        print(f"   ERROR in product search: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print()
    print("=== DEBUG SEARCH COMPLETED ===")

if __name__ == "__main__":
    asyncio.run(debug_search())