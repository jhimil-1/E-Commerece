import requests
import json

# Test the specific issue from the frontend
# The frontend is searching for "phones" but the category is "Smartphones"

# Get token first
login_data = {'username': 'test_user2', 'password': 'test123'}
login_response = requests.post('http://localhost:8000/auth/login', json=login_data)
token = login_response.json()['access_token']

headers = {'Authorization': f'Bearer {token}'}

# Test the exact scenario from the logs
print("=== Testing frontend issue: 'phones' vs 'Smartphones' ===")

queries = [
    # This is what the frontend is searching for (returns 0 results)
    {'query': 'smartphones', 'category': 'phones', 'limit': 20, 'min_score': 0.3},
    
    # This is what should work (returns results)
    {'query': 'smartphones', 'category': 'Smartphones', 'limit': 20, 'min_score': 0.3},
    
    # Test case variations
    {'query': 'smartphones', 'category': 'PHONES', 'limit': 20, 'min_score': 0.3},
    {'query': 'smartphones', 'category': 'Phones', 'limit': 20, 'min_score': 0.3},
]

for i, search_data in enumerate(queries, 1):
    print(f'\n--- Test {i}: Query="{search_data["query"]}", Category="{search_data["category"]}" ---')
    response = requests.post('http://localhost:8000/products/search', data=search_data, headers=headers)
    results = response.json()
    result_count = len(results.get("results", []))
    print(f'Results: {result_count}')
    if result_count > 0:
        print(f'First result: {results["results"][0]["name"]} (category: {results["results"][0]["category"]})')
    else:
        print('No results found')

# Also test what categories are actually available
print("\n=== Testing available categories ===")
available_categories = ['electronics', 'phones', 'smartphones', 'Smartphones', 'PHONES']
for category in available_categories:
    search_data = {'query': 'phone', 'category': category, 'limit': 5, 'min_score': 0.3}
    response = requests.post('http://localhost:8000/products/search', data=search_data, headers=headers)
    results = response.json()
    result_count = len(results.get("results", []))
    print(f'Category "{category}": {result_count} results')

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