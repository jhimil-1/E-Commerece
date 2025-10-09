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
print(f'Results: {len(response.json())}')
if response.json():
    print(f'First result: {response.json()[0]["name"]} (category: {response.json()[0]["category"]})')
else:
    print('No results returned')