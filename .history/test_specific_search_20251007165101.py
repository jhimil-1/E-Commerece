import requests
import json

# Get fresh token first
response = requests.post('http://localhost:8000/token', data={'username': 'test_user2', 'password': 'test123'})
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
    response = requests.post(
        'http://localhost:8000/products/search',
        headers=headers,
        json={"query": query, "category": None, "min_score": 0.1}
    )
    
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Message: {result.get('message', 'No message')}")
    print(f"Count: {result.get('count', 0)}")
    if result.get('results'):
        print(f"First result: {result['results'][0]['name']} (category: {result['results'][0]['category']})")
    else:
        print("No results found")