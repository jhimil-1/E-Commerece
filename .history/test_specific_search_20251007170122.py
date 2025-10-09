import requests

# Get fresh token first
response = requests.post('http://localhost:8000/auth/login', json={'username': 'test_user2', 'password': 'test123'})
token_data = response.json()
ACCESS_TOKEN = token_data['access_token']

# Test different search queries
search_queries = [
    "electronics",
    "laptops", 
    "headphones",
    "smartphones",
    "Laptops",
    "Headphones",
    "Smartphones"
]

headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}

for query in search_queries:
    print(f"\n=== Testing search for: {query} ===")
    
    # Use FormData format like the frontend does
    form_data = {
        'query': query,
        'category': query,  # Use same value for category
        'limit': '10'
    }
    
    response = requests.post(
        'http://localhost:8000/products/search',
        headers=headers,
        data=form_data  # Use data= instead of json=
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code != 200:
        print(f"Error response: {response.text}")
    else:
        result = response.json()
        print(f"Message: {result.get('message', 'No message')}")
        print(f"Count: {result.get('count', 0)}")
        if result.get('results'):
            print(f"First result: {result['results'][0]['name']} (category: {result['results'][0]['category']})")
        else:
            print("No results found")