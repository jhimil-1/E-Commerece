from database import MongoDB

def check_user_by_userid():
    db = MongoDB.get_db()
    
    # Check if user with ID 9ba7d438-2066-4466-991d-e4f78e728a78 exists
    print("Checking user with ID 9ba7d438-2066-4466-991d-e4f78e728a78...")
    user = db.users.find_one({"user_id": "9ba7d438-2066-4466-991d-e4f78e728a78"})
    
    if user:
        print(f"Found user: {user.get('username', 'N/A')} with user_id: {user.get('user_id', 'N/A')}")
    else:
        print("User not found by user_id, checking by _id...")
        try:
            from bson import ObjectId
            user = db.users.find_one({"_id": ObjectId("9ba7d438-2066-4466-991d-e4f78e728a78")})
            if user:
                print(f"Found user by _id: {user.get('username', 'N/A')} with user_id: {user.get('user_id', 'N/A')}")
            else:
                print("User not found by _id either")
        except Exception as e:
            print(f"Error checking by _id: {e}")
    
    # Check products for this user
    print("Checking products for user 9ba7d438-2066-4466-991d-e4f78e728a78...")
    products = list(db.products.find({"created_by": "9ba7d438-2066-4466-991d-e4f78e728a78"}).limit(5))
    
    print(f"Found {len(products)} products for this user:")
    for product in products:
        print(f"- Name: {product.get('name', 'N/A')}")
        print(f"  Category: {product.get('category', 'N/A')}")

if __name__ == "__main__":
    check_user_by_userid()