import requests
import json

# Test the exact scenario from the logs
login_data = {'username': 'testuser1', 'password': 'testpass123'}
login_response = requests.post('http://localhost:8000/auth/login', json=login_data)
token = login_response.json()['access_token']

headers = {'Authorization': f'Bearer {token}'}

# Test different case variations for category
queries = [
    # Test laptops (should work with case-insensitive fix)
    {'query': 'laptop', 'category': 'Laptops', 'limit': 5},
    {'query': 'laptop', 'category': 'laptops', 'limit': 5},
    {'query': 'laptop', 'category': 'LAPTOPS', 'limit': 5},
    
    # Test headphones (should work with case-insensitive fix)
    {'query': 'headphone', 'category': 'Headphones', 'limit': 5},
    {'query': 'headphone', 'category': 'headphones', 'limit': 5},
    
    # Test smartphones (currently returning 0)
    {'query': 'phone', 'category': 'Smartphones', 'limit': 5},
    {'query': 'phone', 'category': 'smartphones', 'limit': 5},
]

for i, search_data in enumerate(queries, 1):
    print(f'\n--- Test {i}: Query={search_data["query"]}, Category={search_data["category"]} ---')
    response = requests.post('http://localhost:8000/products/search', data=search_data, headers=headers)
    results = response.json()
    result_count = len(results.get("results", []))
    print(f'Results: {result_count}')
    if result_count > 0:
        print(f'First result: {results["results"][0]["name"]} (category: {results["results"][0]["category"]})')
    else:
        print('No results found')