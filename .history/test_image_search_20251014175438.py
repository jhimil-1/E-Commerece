import requests
import base64
import json

# Create a simple test image (1x1 red pixel)
test_image_data = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg==')

# Test the image search endpoint
url = "http://localhost:8000/chat/image-query"

# Prepare the request
files = {
    'image': ('test_image.png', test_image_data, 'image/png')
}

data = {
    'query': 'gold necklace',
    'session_id': 'test_session_123'
}

try:
    response = requests.post(url, files=files, data=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Found {len(result.get('products', []))} products")
        for product in result.get('products', [])[:3]:
            print(f"- {product.get('name', 'Unknown')}: ${product.get('price', 'N/A')}")
    else:
        print(f"Error: {response.text}")
        
except Exception as e:
    print(f"Request failed: {e}")