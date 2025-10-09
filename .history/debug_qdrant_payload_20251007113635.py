#!/usr/bin/env python3

import asyncio
from database import MongoDB
from qdrant_utils import qdrant_manager
from clip_utils import clip_manager

async def debug_qdrant_payload():
    """Debug what's actually in Qdrant payload"""
    
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
    
    # Search without user filter first to see what's available
    print("\n=== Search without user filter ===")
    results = qdrant_manager.search_similar_products(
        query_embedding=test_embedding,
        limit=5
    )
    
    print(f"Found {len(results)} results without user filter")
    for i, r in enumerate(results):
        print(f"  {i+1}. {r['name']} (score: {r['score']:.3f})")
        print(f"      Payload keys: {list(r.keys())}")
        if 'created_by' in r:
            print(f"      created_by: {r['created_by']}")
        if 'user_id' in r:
            print(f"      user_id: {r['user_id']}")
    
    # Now search with user filter
    print(f"\n=== Search with user_id filter: {user_id} ===")
    results = qdrant_manager.search_similar_products(
        query_embedding=test_embedding,
        user_id=user_id,
        limit=5
    )
    
    print(f"Found {len(results)} results with user filter")
    for i, r in enumerate(results):
        print(f"  {i+1}. {r['name']} (score: {r['score']:.3f})")

if __name__ == "__main__":
    asyncio.run(debug_qdrant_payload())