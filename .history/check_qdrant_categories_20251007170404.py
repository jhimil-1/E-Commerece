import requests
import json

# Get fresh token first
response = requests.post('http://localhost:8000/auth/login', json={'username': 'test_user2', 'password': 'test123'})
token_data = response.json()
ACCESS_TOKEN = token_data['access_token']

headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}

# Test with different case variations to see what Qdrant contains
test_cases = [
    ("electronics", "electronics"),
    ("Electronics", "Electronics"),
    ("laptops", "laptops"),
    ("Laptops", "Laptops"),
    ("headphones", "headphones"),
    ("Headphones", "Headphones"),
]

for query_text, category in test_cases:
    print(f"\n=== Testing: query='{query_text}', category='{category}' ===")
    
    # Use FormData format like the frontend does
    form_data = {
        'query': query_text,
        'category': category,
        'limit': '10'
    }
    
    response = requests.post(
        'http://localhost:8000/products/search',
        headers=headers,
        data=form_data
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Count: {result.get('count', 0)}")
        if result.get('results'):
            # Show first result's category to understand the case
            first_result = result['results'][0]
            print(f"First result: {first_result['name']} (category: '{first_result['category']}')")
        else:
            print("No results found")
    else:
        print(f"Error: {response.text}")