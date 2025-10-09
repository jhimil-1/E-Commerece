import requests
import json

# Test the exact scenario from the logs
login_data = {'username': 'testuser1', 'password': 'testpass123'}
login_response = requests.post('http://localhost:8000/auth/login', json=login_data)
token = login_response.json()['access_token']

headers = {'Authorization': f'Bearer {token}'}

# The API expects Form data, not JSON
search_data = {
    'query': 'phone',  # This is required!
    'category': 'Smartphones',
    'limit': 40
}

response = requests.post('http://localhost:8000/products/search', data=search_data, headers=headers)
print(f'Status: {response.status_code}')
results = response.json()
print(f'Results: {len(results.get(\"results\", []))}')
print(f'Response: {results}')

# Test without query (this should fail)
print('\n--- Testing without query (should fail) ---')
search_data_no_query = {
    'category': 'Smartphones',
    'limit': 40
}

response2 = requests.post('http://localhost:8000/products/search', data=search_data_no_query, headers=headers)
print(f'Status: {response2.status_code}')
print(f'Response: {response2.json()}')