import requests
import json

# Test the products search endpoint with fresh token
token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0X3VzZXIyIiwidXNlcl9pZCI6IjY4ZGE3NWI0OTRjOWI1ZGJlM2JiNTc5MCIIsImV4cCI6MTc1OTkxMDk0N30.XcQY7utsCkkGDKcKxNHBa9DlHvOY7h86ACTCapuv4gY'

try:
    response = requests.post(
        'http://localhost:8000/products/search',
        headers={'Authorization': f'Bearer {token}'},
        data={'query': 'smartphones', 'limit': 2}
    )
    
    data = response.json()
    print('Response status:', response.status_code)
    
    if 'results' in data:
        print('Results found:', len(data['results']))
        if data['results']:
            for i, result in enumerate(data['results'][:2]):
                print(f'Result {i+1}:')
                print(f'  name: {result.get("name", "N/A")}')
                print(f'  category: {result.get("category", "N/A")}')
                print(f'  image_url: {result.get("image_url", "N/A")}')
                print(f'  image_path: {result.get("image_path", "N/A")}')
                print(f'  image: {result.get("image", "N/A")}')
    else:
        print('Full response:', json.dumps(data, indent=2))
        
except Exception as e:
    print('Error:', e)