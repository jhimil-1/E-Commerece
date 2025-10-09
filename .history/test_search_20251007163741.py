import requests
import json

# Use the token from the environment
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0dXNlcjEiLCJ1c2VyX2lkIjoiMjU2MGU0N2MtZGRlNC00Y2JkLTg3MmYtZDAyMDQyYjU4ZjUwIiwiZXhwIjoxNzU5ODM2OTc5fQ.LL5W9rSFKYLTqWrknL_7V4CFc1Lj1HqmazCyjHiLS_s"

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/x-www-form-urlencoded"
}

# Test search for headphones
data = {
    "query": "headphones",
    "limit": 3
}

print("Testing search for headphones...")
response = requests.post("http://localhost:8000/products/search", headers=headers, data=data)
print(f"Status: {response.status_code}")
print(f"Response: {response.text}")

# Test search for electronics
data2 = {
    "query": "electronics",
    "limit": 5
}

print("\nTesting search for electronics...")
response2 = requests.post("http://localhost:8000/products/search", headers=headers, data=data2)
print(f"Status: {response2.status_code}")
print(f"Response: {response2.text}")

# Test search for laptops
data3 = {
    "query": "laptops",
    "limit": 3
}

print("\nTesting search for laptops...")
response3 = requests.post("http://localhost:8000/products/search", headers=headers, data=data3)
print(f"Status: {response3.status_code}")
print(f"Response: {response3.text}")