#!/usr/bin/env python3
"""
Test script for real image search functionality using the test_image.jpg file
"""

import requests
import json

# Test credentials (from previous successful tests)
USERNAME = "test_user_02ff81cd"
PASSWORD = "test123"

def test_real_image_search():
    """Test image search with a real jewelry image file"""
    
    print("🧪 Testing Real Image Search Functionality...")
    print("=" * 60)
    
    # Step 1: Authenticate
    print("\n1️⃣ Authenticating...")
    auth_response = requests.post(
        "http://localhost:8000/auth/login",
        json={"username": USERNAME, "password": PASSWORD}
    )
    
    if auth_response.status_code != 200:
        print(f"   ❌ Authentication failed: {auth_response.status_code}")
        print(f"   Error: {auth_response.text}")
        return False
    
    auth_data = auth_response.json()
    access_token = auth_data.get("access_token")
    user_id = auth_data.get("user_id")
    print(f"   ✅ Authenticated as {USERNAME}")
    print(f"   Token: {access_token[:50]}...")
    print(f"   User ID: {user_id}")
    
    # Step 2: Create session
    print("\n2️⃣ Creating session...")
    session_response = requests.post(
        "http://localhost:8000/chat/sessions",
        json={"user_id": user_id},
        headers={"Authorization": f"Bearer {access_token}"}
    )
    
    if session_response.status_code != 201:
        print(f"   ❌ Session creation failed: {session_response.status_code}")
        print(f"   Error: {session_response.text}")
        return False
    
    session_id = session_response.json().get("session_id")
    print(f"   ✅ Session created: {session_id}")
    
    # Step 3: Test image search with real image
    print("\n3️⃣ Testing image search with real jewelry image...")
    
    try:
        # Read the test image file
        with open("test-website/test_image.jpg", "rb") as image_file:
            image_data = image_file.read()
        
        # Prepare form data
        files = {
            'image': ('test_image.jpg', image_data, 'image/jpeg')
        }
        
        data = {
            'session_id': session_id,
            'query': 'jewelry necklace ring'  # Broad search query
        }
        
        # Send request
        image_search_response = requests.post(
            "http://localhost:8000/chat/image-query",
            files=files,
            data=data,
            headers={"Authorization": f"Bearer {access_token}"}
        )
        
        print(f"   📤 Image search request sent...")
        print(f"   📊 Status Code: {image_search_response.status_code}")
        
        if image_search_response.status_code == 200:
            results = image_search_response.json()
            products = results.get('products', [])
            
            print(f"   ✅ Image search successful!")
            print(f"   📦 Found {len(products)} products")
            
            if products:
                print("\n   🛍️  Top Products Found:")
                for i, product in enumerate(products[:5]):  # Show top 5 products
                    name = product.get('name', 'Unknown Product')
                    price = product.get('price', 'N/A')
                    category = product.get('category', 'Unknown')
                    print(f"      {i+1}. {name} - ${price} ({category})")
                    
                    # Show product details if available
                    if 'description' in product:
                        desc = product['description'][:100] + "..." if len(product['description']) > 100 else product['description']
                        print(f"         Description: {desc}")
                    if 'image_url' in product:
                        print(f"         Image: {product['image_url']}")
                    print()
            else:
                print("   ℹ️  No products found - this might be expected depending on the test image")
                
            # Show full response for debugging
            print(f"   📄 Full Response Preview:")
            print(f"   {str(results)[:500]}...")
            
        else:
            print(f"   ❌ Image search failed:")
            print(f"   Status: {image_search_response.status_code}")
            print(f"   Error: {image_search_response.text}")
            return False
            
    except FileNotFoundError:
        print("   ❌ Test image file not found at test-website/test_image.jpg")
        return False
    except Exception as e:
        print(f"   ❌ Error reading image file: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 Real Image Search Test Complete!")
    print("✅ The system can successfully process real jewelry images!")
    return True

if __name__ == "__main__":
    success = test_real_image_search()
    if success:
        print("\n✨ All tests passed! Image search is working correctly.")
    else:
        print("\n💥 Some tests failed. Check the logs above.")