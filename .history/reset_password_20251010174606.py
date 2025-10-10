from database import MongoDB
import bcrypt

def reset_password():
    db = MongoDB.get_db()
    
    # Reset password for test_user_02ff81cd
    username = "test_user_02ff81cd"
    new_password = "test123"
    
    # Hash the new password
    hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
    
    # Update the user
    result = db.users.update_one(
        {"username": username},
        {"$set": {"hashed_password": hashed_password.decode('utf-8')}}
    )
    
    if result.modified_count > 0:
        print(f"✓ Password reset successfully for {username}")
        print(f"✓ New password: {new_password}")
    else:
        print(f"✗ Failed to reset password for {username}")

if __name__ == "__main__":
    reset_password()