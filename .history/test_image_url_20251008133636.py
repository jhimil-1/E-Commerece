import requests

# Test if the image URL from the search results is accessible
image_url = 'https://mobitez.in/wp-content/uploads/2024/10/Apple-Iphone-16-pro-Max-G-1.jpg'

try:
    response = requests.head(image_url, timeout=10)
    print(f'Image URL status: {response.status_code}')
    print(f'Content-Type: {response.headers.get("content-type", "N/A")}')
    print(f'Content-Length: {response.headers.get("content-length", "N/A")}')
except Exception as e:
    print(f'Error accessing image: {e}')