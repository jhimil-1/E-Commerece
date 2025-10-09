import requests
import json

# Test various search terms to see what's available
base_url = "http://localhost:8000"

# Test user credentials
test_username = "testuser_new_123"
test_password = "testpass123"

print("Testing various search terms...")

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
test_queries = ["gold ring", "phone", "watch", "jewelry", "ring", "gold", "necklace", "earrings", "bracelet", "diamond"]

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