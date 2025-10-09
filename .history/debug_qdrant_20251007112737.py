#!/usr/bin/env python3

import requests
import json
from database import MongoDB
from qdrant_utils import qdrant_manager
from clip_utils import clip_manager

def debug_qdrant():
    """Debug Qdrant search functionality"""
    
    # Get user ID for testuser1
    db = MongoDB.get_db()
    user = db.users.find_one({'username': 'testuser1'})
    if not user:
        print("testuser1 not found")
        return
    
    user_id = user['user_id']
    print(f"testuser1 user_id: {user_id}")
    
    # Check products in MongoDB
    mongo_products = list(db.products.find({'created_by': user_id}))
    print(f"Products in MongoDB for testuser1: {len(mongo_products)}")
    
    for p in mongo_products[:3]:
        print(f"  - {p['name']}: {p['_id']}")
    
    # Check what's in Qdrant
    try:
        # Get collection info
        collection_info = qdrant_manager.client.get_collection(qdrant_manager.collection_name)
        print(f"\nQdrant collection info:")
        print(f"  Points count: {collection_info.points_count}")
        print(f"  Status: {collection_info.status}")
        
        # Search without user filter first
        test_embedding = clip_manager.get_text_embedding("rings")
        print(f"\nTest embedding generated: {len(test_embedding)} dimensions")
        
        # Search without user filter
        results_no_filter = qdrant_manager.search_similar_products(
            query_embedding=test_embedding,
            user_id=None,  # No user filter
            limit=5
        )
        print(f"Results without user filter: {len(results_no_filter)}")
        for r in results_no_filter[:3]:
            print(f"  - {r['name']} (score: {r['score']:.3f})")
        
        # Search with user filter
        results_with_filter = qdrant_manager.search_similar_products(
            query_embedding=test_embedding,
            user_id=user_id,
            limit=5
        )
        print(f"Results with user filter ({user_id}): {len(results_with_filter)}")
        for r in results_with_filter[:3]:
            print(f"  - {r['name']} (score: {r['score']:.3f})")
        
        # Check if any products exist in Qdrant with this user ID
        from qdrant_client import models
        
        scroll_results = qdrant_manager.client.scroll(
            collection_name=qdrant_manager.collection_name,
            scroll_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="created_by",
                        match=models.MatchValue(value=user_id)
                    )
                ]
            ),
            limit=10
        )
        
        print(f"\nProducts in Qdrant with user_id {user_id}: {len(scroll_results[0])}")
        for point in scroll_results[0][:3]:
            print(f"  - {point.payload.get('name', 'Unknown')}: {point.payload.get('mongo_id', 'no-mongo-id')}")
            
    except Exception as e:
        print(f"Error checking Qdrant: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_qdrant()