#!/usr/bin/env python3

import asyncio
from database import MongoDB
from qdrant_utils import qdrant_manager
from clip_utils import clip_manager

async def debug_qdrant_detailed():
    """Detailed debug of Qdrant search"""
    
    # Get user ID for testuser1
    db = MongoDB.get_db()
    user = db.users.find_one({'username': 'testuser1'})
    if not user:
        print("testuser1 not found")
        return
    
    user_id = user['user_id']
    print(f"testuser1 user_id: {user_id}")
    
    # Generate embedding for "rings"
    test_embedding = clip_manager.get_text_embedding("rings")
    print(f"Generated embedding: {len(test_embedding)} dimensions")
    
    # Test 1: Search with user filter
    print("\n=== Test 1: Search with user filter ===")
    try:
        results = qdrant_manager.search_similar_products(
            query_embedding=test_embedding,
            user_id=user_id,
            limit=5
        )
        print(f"Found {len(results)} results with user filter")
        for r in results:
            print(f"  - {r['name']} (score: {r['score']:.3f})")
    except Exception as e:
        print(f"Error with user filter: {e}")
    
    # Test 2: Search without user filter
    print("\n=== Test 2: Search without user filter ===")
    try:
        results = qdrant_manager.search_similar_products(
            query_embedding=test_embedding,
            limit=5
        )
        print(f"Found {len(results)} results without user filter")
        for r in results:
            print(f"  - {r['name']} (score: {r['score']:.3f})")
    except Exception as e:
        print(f"Error without user filter: {e}")
    
    # Test 3: Get collection info
    print("\n=== Test 3: Collection info ===")
    try:
        info = qdrant_manager.client.get_collection(qdrant_manager.collection_name)
        print(f"Collection status: {info.status}")
        print(f"Points count: {info.points_count}")
        print(f"Vectors count: {info.vectors_count}")
    except Exception as e:
        print(f"Error getting collection info: {e}")
    
    # Test 4: Scroll through all points for this user
    print("\n=== Test 4: Scroll through points for user ===")
    try:
        from qdrant_client import models
        
        scroll_results = qdrant_manager.client.scroll(
            collection_name=qdrant_manager.collection_name,
            scroll_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="user_id",
                        match=models.MatchValue(value=user_id)
                    )
                ]
            ),
            limit=10,
            with_payload=True,
            with_vectors=False
        )
        
        points, next_offset = scroll_results
        print(f"Found {len(points)} points for user")
        
        for point in points:
            payload = point.payload
            print(f"  - {payload.get('name', 'Unknown')} (category: {payload.get('category', 'Unknown')})")
            
    except Exception as e:
        print(f"Error scrolling: {e}")

if __name__ == "__main__":
    asyncio.run(debug_qdrant_detailed())