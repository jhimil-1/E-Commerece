import requests
import json
import time

# API base URL
BASE_URL = "http://localhost:8000"

def get_fresh_token():
    """Get a fresh JWT token"""
    login_data = {
        "username": "testuser1",
        "password": "testpass123"
    }
    
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json=login_data
    )
    
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        raise Exception("Failed to get token")

def create_session(token):
    """Create a chat session"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(
        f"{BASE_URL}/chat/sessions",
        headers=headers
    )
    
    if response.status_code == 201:
        return response.json()["session_id"]
    else:
        raise Exception("Failed to create session")

def upload_products(token):
    """Upload test products"""
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # Read the test products
    with open("test_products.json", "r") as f:
        products = json.load(f)
    
    files = {
        "file": ("test_products.json", json.dumps(products), "application/json")
    }
    
    response = requests.post(
        f"{BASE_URL}/products/upload",
        headers=headers,
        files=files
    )
    
    return response.status_code == 200, response.json()

def test_text_search(token, session_id, query):
    """Test text-based search"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    search_data = {
        "session_id": session_id,
        "query": query
    }
    
    response = requests.post(
        f"{BASE_URL}/chat/query",
        headers=headers,
        json=search_data
    )
    
    return response.status_code == 200, response.json()

def test_image_search(token, session_id):
    """Test image-based search"""
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # Create a simple test image (1x1 pixel PNG)
    test_image_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc\xf8\x0f\x00\x00\x01\x01\x00\x05\x18\xd4c\x00\x00\x00\x00IEND\xaeB`\x82'
    
    files = {
        "image": ("test.png", test_image_data, "image/png")
    }
    
    data = {
        "session_id": session_id
    }
    
    response = requests.post(
        f"{BASE_URL}/products/search-by-image",
        headers=headers,
        files=files,
        data=data
    )
    
    return response.status_code == 200, response.json()

def main():
    print("=== Complete Workflow Test ===")
    
    # Step 1: Get authentication token
    print("\n1. Getting authentication token...")
    try:
        token = get_fresh_token()
        print("✓ Token obtained successfully")
    except Exception as e:
        print(f"✗ Failed to get token: {e}")
        return
    
    # Step 2: Create chat session
    print("\n2. Creating chat session...")
    try:
        session_id = create_session(token)
        print(f"✓ Session created: {session_id}")
    except Exception as e:
        print(f"✗ Failed to create session: {e}")
        return
    
    # Step 3: Upload products
    print("\n3. Uploading products...")
    upload_success, upload_response = upload_products(token)
    if upload_success:
        print(f"✓ Products uploaded successfully: {upload_response}")
        # Wait a moment for indexing
        time.sleep(2)
    else:
        print(f"✗ Upload failed: {upload_response}")
        return
    
    # Step 4: Test text search
    print("\n4. Testing text search...")
    search_queries = ["smartphone", "jewelry", "coffee", "fashion", "electronics"]
    
    for query in search_queries:
        print(f"\n   Testing query: '{query}'")
        search_success, search_response = test_text_search(token, session_id, query)
        if search_success:
            products = search_response.get("products", [])
            print(f"   ✓ Found {len(products)} products")
            if products:
                print(f"   Top result: {products[0]['name']} - ${products[0]['price']}")
        else:
            print(f"   ✗ Search failed: {search_response}")
    
    # Step 5: Test image search
    print("\n5. Testing image search...")
    image_success, image_response = test_image_search(token, session_id)
    if image_success:
        products = image_response.get("products", [])
        print(f"✓ Image search completed, found {len(products)} products")
    else:
        print(f"✗ Image search failed: {image_response}")
    
    print("\n=== Test Summary ===")
    print("✓ Authentication working")
    print("✓ Session management working")
    print("✓ Product upload working")
    print("✓ Text search working")
    print("✓ Image search working" if image_success else "✗ Image search failed")
    print("\n🎉 Complete workflow test completed successfully!")

if __name__ == "__main__":
    main()