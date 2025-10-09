import requests
import json

# API base URL
BASE_URL = "http://localhost:8000"

# Test the token directly
def test_token():
    """Test if the token is valid by creating a session"""
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0dXNlcjEiLCJ1c2VyX2lkIjoiMjU2MGU0N2MtZGRlNC00Y2JkLTg3MmYtZDAyMDQyYjU4ZjUwIiwiZXhwIjoxNzU5ODE1OTUwfQ._SbRZKvH0ZzlJpexAHLp4Cx9hJ1_HqTYm-AXQYRxoa8"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        # Test creating a session
        response = requests.post(
            f"{BASE_URL}/chat/sessions",
            headers=headers
        )
        
        print(f"Session creation test:")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code in [200, 201]:
            print("✓ Token is working!")
            return response.json()["session_id"]
        else:
            print("✗ Token validation failed")
            return None
            
    except Exception as e:
        print(f"Test failed: {e}")
        return None

def test_upload_with_session(session_id):
    """Test product upload with a valid session"""
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0dXNlcjEiLCJ1c2VyX2lkIjoiMjU2MGU0N2MtZGRlNC00Y2JkLTg3MmYtZDAyMDQyYjU4ZjUwIiwiZXhwIjoxNzU5ODE1OTUwfQ._SbRZKvH0ZzlJpexAHLp4Cx9hJ1_HqTYm-AXQYRxoa8"
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        # Read the test products
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
        
        print(f"\nUpload test:")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        return response.status_code == 200
        
    except Exception as e:
        print(f"Upload test failed: {e}")
        return False

def test_search(session_id):
    """Test search functionality"""
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0dXNlcjEiLCJ1c2VyX2lkIjoiMjU2MGU0N2MtZGRlNC00Y2JkLTg3MmYtZDAyMDQyYjU4ZjUwIiwiZXhwIjoxNzU5ODE1OTUwfQ._SbRZKvH0ZzlJpexAHLp4Cx9hJ1_HqTYm-AXQYRxoa8"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        # Test search
        search_data = {
            "session_id": session_id,
            "query": "smartphone"
        }
        
        response = requests.post(
            f"{BASE_URL}/chat/query",
            headers=headers,
            json=search_data
        )
        
        print(f"\nSearch test:")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        return response.status_code == 200
        
    except Exception as e:
        print(f"Search test failed: {e}")
        return False

if __name__ == "__main__":
    print("=== Debugging Authentication ===")
    session_id = test_token()
    
    if session_id:
        print(f"\n=== Testing Upload ===")
        upload_success = test_upload_with_session(session_id)
        
        print(f"\n=== Testing Search ===")
        search_success = test_search(session_id)
        
        if upload_success and search_success:
            print("\n✓ All tests passed!")
        else:
            print(f"\n✗ Some tests failed. Upload: {upload_success}, Search: {search_success}")
    else:
        print("\n✗ Authentication failed - cannot proceed with other tests")