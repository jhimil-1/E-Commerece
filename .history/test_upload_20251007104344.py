import requests
import json

# JWT token from login
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0dXNlcjEiLCJ1c2VyX2lkIjoiMjU2MGU0N2MtZGRlNC00Y2JkLTg3MmYtZDAyMDQyYjU4ZjUwIiwiZXhwIjoxNzU5ODE1ODEzfQ.c5TOj_TMxl9iCS-VaCsKd1H28XrJ9YZ"

# API base URL
BASE_URL = "http://localhost:8000"

# Headers with JWT token
headers = {
    "Authorization": f"Bearer {TOKEN}"
}

def test_product_upload():
    """Test uploading products from JSON file"""
    try:
        # Read the test products JSON file
        with open("test_products.json", "r") as f:
            products = json.load(f)
        
        # Upload products
        files = {
            "file": ("test_products.json", json.dumps(products), "application/json")
        }
        
        response = requests.post(
            f"{BASE_URL}/products/upload",
            headers=headers,
            files=files
        )
        
        print("Upload Response:")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        return response.json() if response.status_code == 200 else None
        
    except Exception as e:
        print(f"Upload test failed: {e}")
        return None

def test_text_search():
    """Test text-based product search"""
    try:
        # First create a session
        session_response = requests.post(
            f"{BASE_URL}/chat/sessions",
            headers=headers
        )
        
        if session_response.status_code != 201:
            print(f"Failed to create session: {session_response.text}")
            return
            
        session_data = session_response.json()
        session_id = session_data["session_id"]
        print(f"Created session: {session_id}")
        
        # Test different search queries
        test_queries = [
            "smartphone",
            "headphones", 
            "gift for birthday",
            "running shoes",
            "coffee maker"
        ]
        
        for query in test_queries:
            print(f"\n--- Testing query: '{query}' ---")
            
            search_data = {
                "session_id": session_id,
                "query": query
            }
            
            response = requests.post(
                f"{BASE_URL}/chat/query",
                headers=headers,
                json=search_data
            )
            
            print(f"Status Code: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                print(f"Response: {result['response']}")
                print(f"Products found: {len(result['products'])}")
                for product in result['products']:
                    print(f"  - {product['name']} (${product['price']}) - Score: {product['similarity_score']:.2f}")
            else:
                print(f"Error: {response.text}")
                
    except Exception as e:
        print(f"Search test failed: {e}")

if __name__ == "__main__":
    print("=== Testing Product Upload ===")
    upload_result = test_product_upload()
    
    print("\n=== Testing Text Search ===")
    test_text_search()