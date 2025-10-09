import requests
import json

# Test the exact scenario from the logs
login_data = {'username': 'testuser1', 'password': 'testpass123'}
login_response = requests.post('http://localhost:8000/auth/login', json=login_data)
token = login_response.json()['access_token']

headers = {'Authorization': f'Bearer {token}'}

# Test different case variations for category
queries = [
    {'query': 'phone', 'category': 'Smartphones', 'limit': 10},
    {'query': 'phone', 'category': 'smartphones', 'limit': 10},
    {'query': 'phone', 'category': 'SMARTPHONES', 'limit': 10},
    {'query': 'phone', 'category': 'SmArTpHoNeS', 'limit': 10},
]

for i, search_data in enumerate(queries, 1):
    print(f'\n--- Test {i}: Category = {search_data["category"]} ---')
    response = requests.post('http://localhost:8000/products/search', data=search_data, headers=headers)
    results = response.json()
    result_count = len(results.get("results", []))
    print(f'Results: {result_count}')
    if result_count > 0:
        print(f'First result: {results["results"][0]["name"]} (category: {results["results"][0]["category"]})')
    else:
        print('No results found')