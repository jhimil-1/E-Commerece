#!/usr/bin/env python3

import asyncio
from database import MongoDB
from qdrant_utils import qdrant_manager
from clip_utils import clip_manager
from qdrant_client import models

async def debug_search_filter():
    """Debug the search filter issue"""
    
    # Get user ID for testuser
    db = MongoDB.get_db()
    user = db.users.find_one({'username': 'testuser'})
    if not user:
        print("testuser not found")
        return
    
    user_id = str(user['_id'])
    print(f"testuser user_id: {user_id}")
    
    # Generate embedding for "rings"
    text_embedding = clip_manager.get_text_embedding("rings")
    print(f"Generated embedding for 'rings', length: {len(text_embedding)}")
    
    # Search with user filter (current approach)
    print("\n=== Search with user filter (current approach) ===")
    try:
        results = qdrant_manager.client.search(
            collection_name=qdrant_manager.collection_name,
            query_vector=text_embedding,
            query_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="created_by",
                        match=models.MatchValue(value=user_id)
                    )
                ]
            ),
            limit=5
        )
        print(f"Results with user_id filter: {len(results)}")
        for result in results:
            print(f"  Score: {result.score}, Payload: {result.payload}")
    except Exception as e:
        print(f"Error with user_id filter: {e}")
    
    # Search with username filter (correct approach)
    print("\n=== Search with username filter (correct approach) ===")
    try:
        results = qdrant_manager.client.search(
            collection_name=qdrant_manager.collection_name,
            query_vector=text_embedding,
            query_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="created_by",
                        match=models.MatchValue(value="testuser")
                    )
                ]
            ),
            limit=5
        )
        print(f"Results with username filter: {len(results)}")
        for result in results:
            print(f"  Score: {result.score}, Payload: {result.payload}")
    except Exception as e:
        print(f"Error with username filter: {e}")
    
    # Search without user filter
    print("\n=== Search without user filter ===")
    try:
        results = qdrant_manager.client.search(
            collection_name=qdrant_manager.collection_name,
            query_vector=text_embedding,
            limit=5
        )
        print(f"Results without user filter: {len(results)}")
        for result in results:
            print(f"  Score: {result.score}, Payload: {result.payload}")
    except Exception as e:
        print(f"Error without user filter: {e}")

if __name__ == "__main__":
    asyncio.run(debug_search_filter())