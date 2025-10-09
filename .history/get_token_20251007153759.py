import requests

# Get fresh token
login_data = {
    "username": "testuser1",
    "password": "testpass1"
}

response = requests.post("http://localhost:8000/auth/login", data=login_data)
print(f"Login response: {response.status_code}")
print(f"Token: {response.json()}")

if response.status_code == 200:
    token = response.json()["access_token"]
    print(f"\nNew token: {token}")
    
    # Test search with new token
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {
        "query": "headphones",
        "limit": 3
    }
    
    search_response = requests.post("http://localhost:8000/products/search", headers=headers, data=data)
    print(f"\nSearch response: {search_response.status_code}")
    print(f"Search results: {search_response.text}")