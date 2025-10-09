import requests
import json

# Test with the working token
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0dXNlcjEiLCJ1c2VyX2lkIjoiMjU2MGU0N2MtZGRlNC00Y2JkLTg3MmYtZDAyMDQyYjU4ZjUwIiwiZXhwIjoxNzI4MzY0MzQwfQ.V8Iun0T0P8F8yVqX8pWB5X8pWB5X8pWB5X8pWB5X8pWB5"

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/x-www-form-urlencoded"
}

# Test broader searches
test_queries = ["smart", "watch", "speaker", "gift", "ring"]

for query in test_queries:
    print(f"\n🔍 Testing search for: {query}")
    data = {
        "query": query,
        "limit": 5
    }
    
    response = requests.post(
        "http://localhost:8000/products/search",
        headers=headers,
        data=data
    )
    
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Message: {result.get('message', 'No message')}")
    print(f"Results count: {len(result.get('results', []))}")
    
    if result.get('results'):
        for i, product in enumerate(result['results'][:3]):
            print(f"  {i+1}. {product.get('name', 'Unknown')} (${product.get('price', 'N/A')}) - Score: {product.get('similarity_score', 0):.3f}")
    else:
        print("  No products found")