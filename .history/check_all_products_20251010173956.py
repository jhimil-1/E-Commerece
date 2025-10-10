from database import MongoDB

def check_all_products():
    db = MongoDB.get_db()
    
    print("Checking all products in MongoDB...")
    products = list(db.products.find({}).limit(10))
    
    if not products:
        print("No products found in MongoDB at all!")
        return
    
    print(f"Found {len(products)} products:")
    for product in products:
        print(f"- Name: {product.get('name', 'N/A')}")
        print(f"  Category: {product.get('category', 'N/A')}")
        print(f"  Created by: {product.get('created_by', 'N/A')}")
        print()
    
    # Check what unique users have products
    print("Checking unique users with products...")
    pipeline = [
        {"$group": {"_id": "$created_by", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    user_counts = list(db.products.aggregate(pipeline))
    
    print(f"Found {len(user_counts)} unique users with products:")
    for user in user_counts:
        user_id = user["_id"]
        count = user["count"]
        print(f"- User ID: {user_id} has {count} products")

if __name__ == "__main__":
    check_all_products()