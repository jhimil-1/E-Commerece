from database import MongoDB

def test_mongodb_direct():
    db = MongoDB.get_db()
    
    # Test user ID
    user_id = "9ba7d438-2066-4466-991d-e4f78e728a78"
    
    print(f"Testing MongoDB direct access for user: {user_id}")
    
    # Check products in MongoDB
    products = list(db.products.find({"created_by": user_id}).limit(5))
    
    print(f"Found {len(products)} products in MongoDB:")
    for product in products:
        print(f"- Name: {product.get('name', 'N/A')}")
        print(f"  Category: {product.get('category', 'N/A')}")
        print(f"  Price: {product.get('price', 'N/A')}")
        print(f"  Image URL: {product.get('image_url', 'N/A')}")
        print(f"  Created by: {product.get('created_by', 'N/A')}")
        print()
    
    # Check if we can get product by name
    print("Testing search by name...")
    search_products = list(db.products.find({
        "created_by": user_id,
        "name": {"$regex": "dress", "$options": "i"}
    }).limit(3))
    
    print(f"Found {len(search_products)} products matching 'dress':")
    for product in search_products:
        print(f"- Name: {product.get('name', 'N/A')}")

if __name__ == "__main__":
    test_mongodb_direct()