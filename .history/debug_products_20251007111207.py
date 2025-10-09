from database import MongoDB
from qdrant_utils import QdrantManager
import json

def debug_products():
    print("=== DEBUGGING PRODUCTS ===")
    
    # Check MongoDB
    db = MongoDB.get_db()
    total_products = db.products.count_documents({})
    print(f"Total products in MongoDB: {total_products}")
    
    # Check products by user
    user_products = db.products.count_documents({"created_by": "testuser1"})
    print(f"Products by testuser1: {user_products}")
    
    # Check products by testuser
    testuser_products = db.products.count_documents({"created_by": "testuser"})
    print(f"Products by testuser: {testuser_products}")
    
    # Show first few products
    products = list(db.products.find().limit(5))
    for i, product in enumerate(products):
        print(f"Product {i+1}: {product.get('name')} - Category: {product.get('category')} - Created by: {product.get('created_by')}")
    
    # Check Qdrant
    qdrant = QdrantManager()
    
    # Get collection info
    try:
        from config import QDRANT_COLLECTION_NAME
        collection_info = qdrant.client.get_collection(QDRANT_COLLECTION_NAME)
        print(f"Qdrant collection '{QDRANT_COLLECTION_NAME}' points: {collection_info.points_count}")
    except Exception as e:
        print(f"Qdrant collection error: {e}")
    
    # Try a simple search
    try:
        search_result = qdrant.search_similar_products(
            query_embedding=[0.1] * 512,  # Dummy embedding
            user_id="testuser",  # Use correct user
            limit=5
        )
        print(f"Qdrant search results for testuser: {len(search_result)}")
        for i, result in enumerate(search_result):
            print(f"  {i+1}. {result.get('payload', {}).get('name', 'Unknown')} - Score: {result.get('score', 0)}")
    except Exception as e:
        print(f"Qdrant search error for testuser: {e}")
    
    # Try search without user filter
    try:
        search_result = qdrant.search_similar_products(
            query_embedding=[0.1] * 512,  # Dummy embedding
            user_id=None,  # No user filter
            limit=5
        )
        print(f"Qdrant search results without user filter: {len(search_result)}")
        for i, result in enumerate(search_result):
            print(f"  {i+1}. {result.get('payload', {}).get('name', 'Unknown')} - Score: {result.get('score', 0)}")
    except Exception as e:
        print(f"Qdrant search error without user filter: {e}")
    
    # Test with real text embedding
    try:
        from clip_utils import CLIPManager
        clip_manager = CLIPManager()
        text_embedding = clip_manager.get_text_embedding("rings")
        
        search_result = qdrant.search_similar_products(
            query_embedding=text_embedding,
            user_id="testuser",  # Use correct user
            limit=5
        )
        print(f"Qdrant search results for 'rings' with testuser: {len(search_result)}")
        for i, result in enumerate(search_result):
            print(f"  {i+1}. Name: {result.get('name', 'Unknown')} - Category: {result.get('category', 'Unknown')} - Created by: {result.get('created_by', 'Unknown')} - Score: {result.get('score', 0)}")
    except Exception as e:
        print(f"Qdrant text search error: {e}")

if __name__ == "__main__":
    debug_products()