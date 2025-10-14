from database import MongoDB
from bson import ObjectId

def check_phone_products():
    try:
        mongo = MongoDB()
        db = mongo.get_db()
        
        # Check for products with "phone" or "smartphone" in name or description
        phone_products = list(db.products.find({
            "$or": [
                {"name": {"$regex": "phone|smartphone|mobile", "$options": "i"}},
                {"description": {"$regex": "phone|smartphone|mobile", "$options": "i"}}
            ]
        }))
        
        print(f"Found {len(phone_products)} products containing 'phone' or 'smartphone':")
        for product in phone_products:
            print(f" - {product['name']}: {product['description'][:100]}...")
        
        # List all categories
        categories = db.products.distinct("category")
        print(f"\nAll categories in database: {categories}")
        
        # Check electronics category specifically
        electronics_products = list(db.products.find({"category": "electronics"}).limit(10))
        print(f"\nFirst 10 electronics products:")
        for product in electronics_products:
            print(f" - {product['name']}: {product['description'][:100]}...")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_phone_products()