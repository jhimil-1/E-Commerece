import requests
import json
import sys

def test_frontend_upload():
    # Login first
    login_data = {
        "username": "test_user2",
        "password": "testpass123"
    }
    
    try:
        # Login
        response = requests.post("http://localhost:8000/auth/login", json=login_data)
        if response.status_code != 200:
            print(f"❌ Login failed: {response.status_code} - {response.text}")
            return False
            
        login_result = response.json()
        token = login_result["access_token"]
        print(f"✓ Login successful, token: {token[:20]}...")
        
        # Load test products
        with open("test_products.json", "r") as f:
            products = json.load(f)
        
        # Upload products (simulating frontend API call)
        headers = {"Authorization": f"Bearer {token}"}
        upload_data = {"products": products}
        
        response = requests.post(
            "http://localhost:8000/products/upload",
            headers=headers,
            json=upload_data
        )
        
        if response.status_code != 200:
            print(f"❌ Upload failed: {response.status_code} - {response.text}")
            return False
            
        result = response.json()
        print(f"✓ Upload response: {json.dumps(result, indent=2)}")
        
        # Check if the response has the correct structure
        if "details" in result and "inserted_count" in result["details"]:
            count = result["details"]["inserted_count"]
            print(f"✅ Frontend upload test passed! Inserted count: {count}")
            return True
        else:
            print(f"❌ Response structure issue: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_frontend_upload()
    sys.exit(0 if success else 1)