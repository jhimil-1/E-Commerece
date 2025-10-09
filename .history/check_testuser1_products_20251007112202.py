#!/usr/bin/env python3

from database import MongoDB

def check_testuser1_products():
    db = MongoDB.get_db()
    
    # Check products created by testuser1
    products = list(db.products.find({"created_by": "testuser1"}))
    
    print(f"Products created by testuser1: {len(products)}")
    
    for product in products:
        print(f"- {product['name']} - Category: {product['category']} - ID: {str(product['_id'])}")
    
    # Check Qdrant points for these products
    from qdrant_utils import qdrant_manager
    
    if products:
        print(f"\nQdrant search for testuser1 products:")
        
        # Search for rings
        import clip
        clip_manager = clip.CLIPManager()
        query_embedding = clip_manager.get_text_embedding("rings")
        
        results = qdrant_manager.search_similar_products(
            query_embedding=query_embedding,
            user_id="testuser1",
            limit=5
        )
        
        print(f"Found {len(results)} results for 'rings' as testuser1:")
        for result in results:
            print(f"  - {result['name']} - Category: {result['category']} - Score: {result['score']}")

if __name__ == "__main__":
    check_testuser1_products()