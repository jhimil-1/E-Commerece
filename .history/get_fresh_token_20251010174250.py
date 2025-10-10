import requests
import json

# Login to get fresh token
login_data = {'username': 'test_user_02ff81cd', 'password': 'test123'}
print(f"Attempting login with: {login_data}")
login_response = requests.post('http://localhost:8000/auth/login', json=login_data)

print(f"Login response status: {login_response.status_code}")
print(f"Login response: {login_response.text}")

if login_response.status_code == 200:
    token_data = login_response.json()
    token = token_data['access_token']
    print(f"Fresh token: {token}")
else:
    print(f"Login failed: {login_response.status_code} - {login_response.text}")
    exit(1)# Test chat query endpoint
    print("\nCreating chat session...")
    session_response = requests.post(
        'http://localhost:8000/chat/sessions',
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
    )

    if session_response.status_code not in [200, 201]:
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
                print(f"Image URL: {products[0].get('image_url', 'N/A')}")
                print(f"Image Path: {products[0].get('image_path', 'N/A')}")
                print(f"Image: {products[0].get('image', 'N/A')}")
                print(f"First product payload: {products[0].get('payload', {})}")
                
                # Check if payload contains image info
                payload = products[0].get('payload', {})
                if isinstance(payload, dict):
                    print(f"Payload keys: {list(payload.keys())}")
                    if 'image_url' in payload:
                        print(f"Image URL in payload: {payload['image_url']}")
                    if 'image_path' in payload:
                        print(f"Image path in payload: {payload['image_path']}")
                    if 'image' in payload:
                        print(f"Image in payload: {payload['image']}")
        
        if 'similar_products' in data:
            similar_products = data['similar_products']
            print(f"Found {len(similar_products)} products in 'similar_products' key")
            if similar_products:
                print(f"First similar product keys: {list(similar_products[0].keys())}")
                print(f"First similar product name: {similar_products[0].get('name', 'N/A')}")
                print(f"First similar product image_url: {similar_products[0].get('image_url', 'N/A')}")
    else:
        print(f"Error: {response.text}")
else:
    print(f"Login failed: {login_response.status_code} - {login_response.text}")