import requests
import json

# Use the fresh token from the PowerShell output
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0X3VzZXIyIiwidXNlcl9pZCI6IjY4ZGE3NWI0OTRjOWI1ZGJlM2JiNTc5MCIsImV4cCI6..."

# First create a session
print("Creating chat session...")
session_response = requests.post(
    'http://localhost:8000/chat/sessions',
    headers={
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
)

if session_response.status_code != 200:
    print(f"Failed to create session: {session_response.status_code} - {session_response.text}")
    exit(1)

session_data = session_response.json()
session_id = session_data['session_id']
print(f"Session created: {session_id}")

# Now test the chat query endpoint
print("\nTesting chat query endpoint...")
query_data = {
    "query": "smartphones",
    "session_id": session_id,
    "limit": 2
}

response = requests.post(
    'http://localhost:8000/chat/query',
    headers={
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    },
    json=query_data
)

print(f"Chat query status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"Response keys: {list(data.keys())}")
    
    # Check for products in different possible locations
    if 'products' in data:
        products = data['products']
        print(f"Found {len(products)} products in 'products' key")
        if products:
            print(f"First product keys: {list(products[0].keys())}")
            print(f"First product name: {products[0].get('name', 'N/A')}")
            print(f"First product image_url: {products[0].get('image_url', 'N/A')}")
    
    if 'similar_products' in data:
        similar_products = data['similar_products']
        print(f"Found {len(similar_products)} products in 'similar_products' key")
        if similar_products:
            print(f"First similar product keys: {list(similar_products[0].keys())}")
            print(f"First similar product name: {similar_products[0].get('name', 'N/A')}")
            print(f"First similar product image_url: {similar_products[0].get('image_url', 'N/A')}")
else:
    print(f"Error: {response.text}")