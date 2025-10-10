import requests

def verify_session_fix():
    # Login with the user who has products
    login_data = {'username': 'test_user_02ff81cd', 'password': 'test123'}
    login_response = requests.post('http://localhost:8000/auth/login', json=login_data)
    
    if login_response.status_code != 200:
        print(f"Login failed: {login_response.status_code}")
        return
    
    token_data = login_response.json()
    token = token_data['access_token']
    user_id_from_token = token_data['user_id']
    
    print(f"User ID from token: {user_id_from_token}")
    
    # Create session
    session_response = requests.post(
        'http://localhost:8000/chat/sessions',
        headers={'Authorization': f'Bearer {token}'}
    )
    
    if session_response.status_code not in [200, 201]:
        print(f"Session creation failed: {session_response.status_code}")
        return
    
    session_data = session_response.json()
    session_id = session_data['session_id']
    
    print(f"Session created: {session_id}")
    
    # Test a query that should find products
    query_data = {
        "query": "clothing",
        "session_id": session_id,
        "limit": 3
    }
    
    response = requests.post(
        'http://localhost:8000/chat/query',
        headers={'Authorization': f'Bearer {token}'},
        json=query_data
    )
    
    print(f"Query response status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        products = data.get('products', [])
        print(f"Found {len(products)} products for user {user_id_from_token}")
        
        if products:
            print("First product details:")
            product = products[0]
            print(f"  Name: {product.get('name')}")
            print(f"  Category: {product.get('category')}")
            print(f"  Image URL: {product.get('image_url')}")
            print(f"  Created by: {product.get('created_by')}")
            
            # Verify the created_by matches the user_id
            if product.get('created_by') == user_id_from_token:
                print("  ✓ Product created_by matches user_id - filtering is working!")
            else:
                print("  ✗ Product created_by doesn't match user_id - filtering issue!")
    else:
        print(f"Query failed: {response.text}")

if __name__ == "__main__":
    verify_session_fix()