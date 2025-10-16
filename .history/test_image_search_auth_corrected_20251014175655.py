import requests
import json
import base64

# Create a simple 1x1 red pixel image for testing
red_pixel_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="

# First, authenticate to get a token
auth_data = {
    "username": "test_user2",
    "password": "test123"
}

print("Authenticating...")
try:
    auth_response = requests.post("http://localhost:8000/auth/login", json=auth_data)
    print(f"Auth response status: {auth_response.status_code}")
    
    if auth_response.status_code == 200:
        auth_result = auth_response.json()
        print(f"Auth successful: {auth_result}")
        
        # Create a session
        print("\nCreating session...")
        session_response = requests.post(
            "http://localhost:8000/chat/sessions",
            headers={"Authorization": f"Bearer {auth_result['access_token']}"}
        )
        print(f"Session response status: {session_response.status_code}")
        
        if session_response.status_code == 201:
            session_data = session_response.json()
            print(f"Session created: {session_data}")
            
            # Now test image search
            print("\nTesting image search...")
            
            # Prepare the image search data
            files = {
                'image': ('test.png', base64.b64decode(red_pixel_base64), 'image/png')
            }
            
            data = {
                'session_id': session_data['session_id'],
                'query': 'gold necklace',
                'category': 'jewellery'
            }
            
            image_search_response = requests.post(
                "http://localhost:8000/chat/image-query",
                headers={"Authorization": f"Bearer {auth_result['access_token']}"},
                files=files,
                data=data
            )
            
            print(f"Image search response status: {image_search_response.status_code}")
            
            if image_search_response.status_code == 200:
                result = image_search_response.json()
                print(f"Image search successful!")
                print(f"Found {len(result.get('products', []))} products")
                if result.get('products'):
                    for product in result['products']:
                        print(f"- {product.get('name', 'Unknown')}: {product.get('price', 'N/A')}")
            else:
                print(f"Image search failed: {image_search_response.text}")
        else:
            print(f"Session creation failed: {session_response.text}")
    else:
        print(f"Authentication failed: {auth_response.text}")
        
except Exception as e:
    print(f"Error: {str(e)}")