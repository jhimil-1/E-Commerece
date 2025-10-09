import requests
import json

# Use the same credentials as the working script
login_data = {'username': 'test_user2', 'password': 'test123'}
login_response = requests.post('http://localhost:8000/auth/login', json=login_data)
token = login_response.json()['access_token']

headers = {'Authorization': f'Bearer {token}'}

# Test the specific scenario from the logs that was failing
# User 68da75b494c9b5dbe3bb5790 searching for Smartphones
print("=== Testing case-insensitive fix for user 68da75b494c9b5dbe3bb5790 ===")

# Test different case variations for smartphones specifically
queries = [
    # Test the exact scenario from logs: Smartphones category
    {'query': 'phone', 'category': 'Smartphones', 'limit': 10, 'user_id': '68da75b494c9b5dbe3bb5790'},
    {'query': 'phone', 'category': 'smartphones', 'limit': 10, 'user_id': '68da75b494c9b5dbe3bb5790'},
    {'query': 'phone', 'category': 'SMARTPHONES', 'limit': 10, 'user_id': '68da75b494c9b5dbe3bb5790'},
    
    # Test other categories to verify case-insensitive fix works
    {'query': 'laptop', 'category': 'Laptops', 'limit': 5, 'user_id': '68da75b494c9b5dbe3bb5790'},
    {'query': 'laptop', 'category': 'laptops', 'limit': 5, 'user_id': '68da75b494c9b5dbe3bb5790'},
    {'query': 'headphone', 'category': 'Headphones', 'limit': 5, 'user_id': '68da75b494c9b5dbe3bb5790'},
    {'query': 'headphone', 'category': 'headphones', 'limit': 5, 'user_id': '68da75b494c9b5dbe3bb5790'},
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