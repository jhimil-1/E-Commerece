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
    
    # Show first few products
    products = list(db.products.find().limit(5))
    for i, product in enumerate(products):
        print(f"Product {i+1}: {product.get('name')} - Category: {product.get('category')} - Created by: {product.get('created_by')}")
    
    # Check Qdrant
    qdrant = QdrantManager()
    
    # Get collection info
    try:
        collection_info = qdrant.client.get_collection("products")
        print(f"Qdrant collection points: {collection_info.points_count}")
    except Exception as e:
        print(f"Qdrant collection error: {e}")
    
    # Try a simple search
    try:
        search_result = qdrant.search_similar_products(
            query_embedding=[0.1] * 512,  # Dummy embedding
            user_id="testuser1",
            limit=5
        )
        print(f"Qdrant search results: {len(search_result)}")
        for i, result in enumerate(search_result):
            print(f"  {i+1}. {result.payload.get('name')} - Score: {result.score}")
    except Exception as e:
        print(f"Qdrant search error: {e}")

if __name__ == "__main__":
    debug_products()