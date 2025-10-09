import requests

# Login
login_data = {'username': 'test_user2', 'password': 'test123'}
response = requests.post('http://localhost:8000/auth/login', json=login_data)
token = response.json()['access_token']
headers = {'Authorization': f'Bearer ' + token}

# Test both cases
for category in ['Laptops', 'laptops']:
    form_data = {'query': category, 'category': category, 'limit': 50}
    response = requests.post('http://localhost:8000/products/search', data=form_data, headers=headers)
    result = response.json()
    print(f'{category}: {result.get("count", 0)} results')
    if result.get('results'):
        # Show first few categories to understand the data
        categories = [p.get('category') for p in result.get('results', [])[:10]]
        print(f'  Categories found: {categories}')
        # Show all unique categories
        unique_categories = list(set([p.get('category') for p in result.get('results', [])]))
        print(f'  All unique categories: {unique_categories}')