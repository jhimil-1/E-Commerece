import requests
import json

# Test JSON upload functionality
BASE_URL = "http://localhost:8000"

# Test user credentials
USERNAME = "testuser1"
PASSWORD = "testpassword123"

def test_json_upload():
    # Step 1: Login to get authentication token
    login_data = {
        "username": USERNAME,
        "password": PASSWORD
    }
    
    print(f"Attempting to login as {USERNAME}...")
    login_response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    
    if login_response.status_code != 200:
        print(f"Login failed: {login_response.status_code}")
        print(f"Response: {login_response.text}")
        return False
    
    auth_data = login_response.json()
    token = auth_data.get("access_token")
    print(f"✓ Login successful! Token: {token[:20]}...")
    
    # Step 2: Load test JSON data
    try:
        with open("test_products.json", "r") as f:
            products_data = json.load(f)
        print(f"✓ Loaded {len(products_data['products'])} products from test_products.json")
    except Exception as e:
        print(f"✗ Failed to load JSON file: {e}")
        return False
    
    # Step 3: Upload products
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    print("Uploading products...")
    upload_response = requests.post(
        f"{BASE_URL}/products/upload", 
        json=products_data,
        headers=headers
    )
    
    print(f"Upload response status: {upload_response.status_code}")
    print(f"Upload response: {upload_response.text}")
    
    if upload_response.status_code == 200:
        result = upload_response.json()
        print(f"✓ Upload successful!")
        print(f"  - Products uploaded: {result.get('uploaded', 0)}")
        print(f"  - Errors: {result.get('errors', [])}")
        return True
    else:
        print(f"✗ Upload failed with status {upload_response.status_code}")
        return False

if __name__ == "__main__":
    test_json_upload()