import requests
import json

# Test edge cases for case-insensitive category search
def test_edge_cases():
    # Login first
    login_data = {
        "username": "test_user2",
        "password": "test123"
    }
    
    response = requests.post("http://localhost:8000/auth/login", data=login_data)
    if response.status_code != 200:
        print(f"Login failed: {response.status_code}")
        return
    
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test various case combinations
    test_cases = [
        "laptops", "Laptops", "LAPTOPS", "LapTopS",
        "headphones", "Headphones", "HEADPHONES", "HeAdPhOnEs",
        "smartphones", "Smartphones", "SMARTPHONES", "SmArTpHoNeS",
        "electronics", "Electronics", "ELECTRONICS"  # Should return 0 as no such category exists
    ]
    
    for category in test_cases:
        form_data = {
            "query": category,
            "category": category,
            "limit": 5
        }
        
        response = requests.post(
            "http://localhost:8000/products/search",
            data=form_data,
            headers=headers
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"=== Testing: {category} ===")
            print(f"Status: {response.status_code}")
            print(f"Count: {result.get('count', 0)}")
            if result.get('count', 0) > 0:
                first_product = result.get('results', [])[0]
                print(f"First result: {first_product.get('name', 'N/A')} (category: '{first_product.get('category', 'N/A')}')")
            else:
                print("No results found")
            print()
        else:
            print(f"=== Testing: {category} ===")
            print(f"Status: {response.status_code}")
            print(f"Error: {response.text}")
            print()

if __name__ == "__main__":
    test_edge_cases()