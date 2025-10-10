from database import MongoDB

def check_users():
    db = MongoDB.get_db()
    
    print("Checking users in database...")
    users = list(db.users.find({}))
    
    if not users:
        print("No users found in database!")
        return
    
    print(f"Found {len(users)} users:")
    for user in users:
        print(f"- Username: {user.get('username', 'N/A')}")
        print(f"  User ID: {user.get('user_id', 'N/A')}")
        print(f"  MongoDB ID: {str(user.get('_id', 'N/A'))}")
        print()

if __name__ == "__main__":
    check_users()