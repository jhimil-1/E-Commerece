from database import MongoDB
from qdrant_client import QdrantClient
from config import QDRANT_HOST, QDRANT_PORT, QDRANT_COLLECTION_NAME

def check_user_products():
    # Check MongoDB products
    db = MongoDB.get_db()
    
    print("Checking products in MongoDB for testuser...")
    products = list(db.products.find({"created_by": "7b2a153b-6586-4120-b537-f8e351f81ec2"}))
    
    if not products:
        print("No products found in MongoDB for testuser!")
    else:
        print(f"Found {len(products)} products in MongoDB:")
        for product in products:
            print(f"- Name: {product.get('name', 'N/A')}")
            print(f"  Category: {product.get('category', 'N/A')}")
            print(f"  Created by: {product.get('created_by', 'N/A')}")
            print()
    
    # Check Qdrant products
    print("Checking products in Qdrant for testuser...")
    try:
        client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
        
        # Search with user filter
        search_result = client.scroll(
            collection_name=QDRANT_COLLECTION_NAME,
            scroll_filter={
                "must": [
                    {
                        "key": "created_by",
                        "match": {"value": "7b2a153b-6586-4120-b537-f8e351f81ec2"}
                    }
                ]
            },
            limit=10
        )
        
        if search_result and search_result[0]:
            print(f"Found {len(search_result[0])} products in Qdrant:")
            for point in search_result[0]:
                payload = point.payload
                print(f"- Name: {payload.get('name', 'N/A')}")
                print(f"  Category: {payload.get('category', 'N/A')}")
                print(f"  Created by: {payload.get('created_by', 'N/A')}")
                print()
        else:
            print("No products found in Qdrant for testuser!")
            
    except Exception as e:
        print(f"Error checking Qdrant: {e}")

if __name__ == "__main__":
    check_user_products()