import requests
import json
import uuid

# Test various search terms with a fresh user
base_url = "http://localhost:8000"

# Create fresh test user credentials
unique_id = str(uuid.uuid4())[:8]
test_username = f"testuser_{unique_id}"
test_email = f"{test_username}@test.com"
test_password = "testpass123"

print(f"Creating fresh user: {test_username}")

# Signup first
signup_response = requests.post(f"{base_url}/auth/signup", json={
    "username": test_username,
    "email": test_email,
    "password": test_password
})

if signup_response.status_code != 200:
    print(f"Signup failed: {signup_response.status_code}")
    print(f"Response: {signup_response.text}")
    # Try login with existing user
    print("Trying login instead...")
else:
    print("Signup successful!")

# Login to get token
login_response = requests.post(f"{base_url}/auth/login", json={
    "username": test_username,
    "password": test_password
})

if login_response.status_code != 200:
    print(f"Login failed: {login_response.status_code}")
    print(f"Response: {login_response.text}")
    exit()

token = login_response.json()["access_token"]
print(f"Got token: {token[:20]}...")

# Create session
session_response = requests.post(f"{base_url}/chat/sessions", headers={
    "Authorization": f"Bearer {token}"
})

if session_response.status_code != 201:
    print(f"Session creation failed: {session_response.status_code}")
    print(f"Response: {session_response.text}")
    exit()

session_id = session_response.json()["session_id"]
print(f"Using session: {session_id}")

# Test various search terms
test_queries = ["gold ring", "phone", "watch", "jewelry", "ring", "gold", "necklace", "earrings", "bracelet", "diamond", "apple", "smartwatch"]

print(f"\n=== Testing {len(test_queries)} different search terms ===")

for query in test_queries:
    print(f"\n--- Testing: '{query}' ---")
    
    search_response = requests.post(f"{base_url}/chat/query", 
        headers={"Authorization": f"Bearer {token}"},
        json={
            "query": query,
            "session_id": session_id,
            "limit": 5
        }
    )
    
    if search_response.status_code == 200:
        data = search_response.json()
        products = data.get("products", [])
        print(f"Found {len(products)} products")
        
        if products:
            for i, product in enumerate(products[:3]):  # Show first 3
                print(f"  {i+1}. {product.get('name', 'Unknown')} - {product.get('category', 'Unknown')} - ${product.get('price', 'N/A')}")
        else:
            print("  No products found")
    else:
        print(f"Search failed: {search_response.status_code}")
        print(f"Error: {search_response.text}")

print(f"\n=== Test completed ===")
print(f"User: {test_username}")
print(f"Session: {session_id}")