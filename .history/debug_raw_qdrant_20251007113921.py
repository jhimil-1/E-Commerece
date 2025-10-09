#!/usr/bin/env python3

import asyncio
from database import MongoDB
from qdrant_utils import qdrant_manager
from clip_utils import clip_manager
from qdrant_client import models

async def debug_raw_qdrant():
    """Debug raw Qdrant points"""
    
    # Get user ID for testuser (not testuser1)
    db = MongoDB.get_db()
    user = db.users.find_one({'username': 'testuser'})
    if not user:
        print("testuser not found")
        return
    
    user_id = user['user_id']
    print(f"testuser user_id: {user_id}")
    
    # Get a product from MongoDB to find its Qdrant point
    product = db.products.find_one({"created_by": "testuser"})
    if not product:
        print("No products found for testuser")
        return
    
    product_id = str(product['_id'])
    print(f"Product ID: {product_id}")
    print(f"Product name: {product['name']}")
    print(f"Product created_by: {product['created_by']}")
    
    # Calculate the Qdrant point ID (same as in upsert_product)
    import hashlib
    point_id = int(hashlib.md5(product_id.encode()).hexdigest(), 16) % (10**18)
    print(f"Expected Qdrant point ID: {point_id}")
    
    # Try to retrieve the raw point
    try:
        result = qdrant_manager.client.retrieve(
            collection_name=qdrant_manager.collection_name,
            ids=[point_id],
            with_payload=True,
            with_vectors=False
        )
        
        if result:
            print(f"Found Qdrant point!")
            print(f"Point ID: {result[0].id}")
            print(f"Payload: {result[0].payload}")
        else:
            print("No Qdrant point found with calculated ID")
            
            # Try to find it by scrolling
            scroll_results = qdrant_manager.client.scroll(
                collection_name=qdrant_manager.collection_name,
                limit=10,
                with_payload=True,
                with_vectors=False
            )
            
            points, next_offset = scroll_results
            print(f"\nFirst 10 points in collection:")
            for point in points:
                if point.payload.get('mongo_id') == product_id:
                    print(f"FOUND! Point ID: {point.id}")
                    print(f"Payload: {point.payload}")
                    break
                else:
                    print(f"Point ID: {point.id}, mongo_id: {point.payload.get('mongo_id')}")
                    
    except Exception as e:
        print(f"Error retrieving point: {e}")

if __name__ == "__main__":
    asyncio.run(debug_raw_qdrant())