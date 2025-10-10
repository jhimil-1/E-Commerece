from database import MongoDB
import bcrypt

def find_user_with_known_password():
    db = MongoDB.get_db()
    
    # Find all users
    users = list(db.users.find({}))
    
    print(f"Found {len(users)} users:")
    
    for user in users:
        username = user['username']
        user_id = user.get('user_id', 'N/A')
        print(f"\nTesting user: {username} (user_id: {user_id})")
        
        # Test with common passwords
        test_passwords = ["test123", "password", "test", "123456", username, "Test123", "Password1"]
        
        for test_pwd in test_passwords:
            try:
                if bcrypt.checkpw(test_pwd.encode('utf-8'), user['hashed_password'].encode('utf-8')):
                    print(f"  ✓ Password found: {test_pwd}")
                    print(f"  ✓ This user has products: {check_user_products(user_id)}")
                    return username, test_pwd
                    break
            except Exception as e:
                print(f"  Error with password {test_pwd}: {e}")
        else:
            print(f"  ✗ No common password found")

def check_user_products(user_id):
    db = MongoDB.get_db()
    count = db.products.count_documents({"created_by": user_id})
    return count > 0

if __name__ == "__main__":
    result = find_user_with_known_password()
    if result:
        username, password = result
        print(f"\n✓ Found working user: {username} with password: {password}")
    else:
        print("\n✗ No user with known password found")