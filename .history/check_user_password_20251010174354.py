from database import MongoDB
import bcrypt

def check_user_password():
    db = MongoDB.get_db()
    
    # Find the user
    user = db.users.find_one({"username": "test_user_02ff81cd"})
    
    if user:
        print(f"Found user: {user['username']}")
        print(f"User ID: {user.get('user_id', 'N/A')}")
        print(f"Hashed password: {user['hashed_password'][:20]}...")
        
        # Test with common passwords
        test_passwords = ["test123", "password", "test", "123456", "test_user_02ff81cd"]
        
        for test_pwd in test_passwords:
            if bcrypt.checkpw(test_pwd.encode('utf-8'), user['hashed_password']):
                print(f"Password is: {test_pwd}")
                break
        else:
            print("Password not found in common passwords")
    else:
        print("User not found")

if __name__ == "__main__":
    check_user_password()