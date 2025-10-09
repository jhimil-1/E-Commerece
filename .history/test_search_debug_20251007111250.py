import requests
import json
import base64

def test_complete_workflow():
    """Test the complete workflow with detailed debugging"""
    
    # Get auth token
    login_response = requests.post(
        "http://localhost:8000/auth/login",
        json={"username": "testuser", "password": "testpass123"}
    )
    print(f"Login status: {login_response.status_code}")
    print(f"Login response: {login_response.text}")
    
    if login_response.status_code != 200:
        print("Login failed, cannot continue")
        return
    
    login_data = login_response.json()
    token = login_data.get("access_token")
    if not token:
        print("No access token in login response")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create session
    session_response = requests.post(
        "http://localhost:8000/chat/sessions",
        headers=headers
    )
    session_id = session_response.json()["session_id"]
    
    # Upload products
    with open("test_products.json", "rb") as f:
        files = {"file": ("test_products.json", f, "application/json")}
        upload_response = requests.post(
            "http://localhost:8000/products/upload",
            headers=headers,
            files=files
        )
    print(f"Upload response: {upload_response.status_code}")
    if upload_response.status_code == 200:
        print(f"Upload data: {upload_response.json()}")
    else:
        print(f"Upload error: {upload_response.text}")
    
    # Test search with debugging
    search_queries = ["rings", "necklaces", "earrings", "bracelets", "jewelry"]
    
    for query in search_queries:
        print(f"\n=== Testing search for: '{query}' ===")
        
        # Test direct product search
        search_response = requests.post(
            "http://localhost:8000/products/search",
            headers=headers,
            data={"query": query, "limit": "10"}
        )
        
        print(f"Search status: {search_response.status_code}")
        if search_response.status_code == 200:
            search_data = search_response.json()
            print(f"Search results count: {search_data.get('count', 0)}")
            print(f"Search message: {search_data.get('message', 'No message')}")
            
            results = search_data.get('results', [])
            print(f"Found {len(results)} products:")
            for i, product in enumerate(results):
                print(f"  {i+1}. {product.get('name', 'Unknown')} - {product.get('category', 'Unknown')} - Score: {product.get('similarity_score', 0)}")
        else:
            print(f"Search error: {search_response.text}")
        
        # Test chatbot search
        chat_response = requests.post(
            "http://localhost:8000/chat/query",
            headers=headers,
            json={"session_id": session_id, "query": f"Show me some {query}"}
        )
        
        print(f"Chat search status: {chat_response.status_code}")
        if chat_response.status_code == 200:
            chat_data = chat_response.json()
            print(f"Chat response: {chat_data.get('response', 'No response')}")
        else:
            print(f"Chat search error: {chat_response.text}")

if __name__ == "__main__":
    test_complete_workflow()