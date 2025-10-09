import requests
import json

# Test the exact scenario from the logs
login_data = {'username': 'testuser1', 'password': 'testpass123'}
login_response = requests.post('http://localhost:8000/auth/login', json=login_data)
token = login_response.json()['access_token']

headers = {'Authorization': f'Bearer {token}'}
search_data = {
    'query': 'phone',
    'category': 'Smartphones',
    'limit': 40,
    'min_score': 0.3
}

response = requests.post('http://localhost:8000/products/search', json=search_data, headers=headers)
print(f'Status: {response.status_code}')
results = response.json()
print(f'Results: {len(results)}')
print(f'Response type: {type(results)}')
print(f'Response content: {results}')
if isinstance(results, list) and len(results) > 0:
    print(f'First result: {results[0]["name"]} (category: {results[0]["category"]})')
elif isinstance(results, dict):
    print(f'Response is dict: {results}')
else:
    print('No results returned or unexpected format')