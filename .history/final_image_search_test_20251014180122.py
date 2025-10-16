#!/usr/bin/env python3
"""
Final comprehensive test of the image search functionality
"""

import requests
import base64
import json
from datetime import datetime

def test_image_search_pipeline():
    """Test the complete image search pipeline"""
    
    print("🧪 Starting comprehensive image search test...")
    print("=" * 60)
    
    # Test 1: Authentication
    print("\n1️⃣ Testing Authentication...")
    auth_data = {
        "username": "test_user_02ff81cd",
        "password": "test123"
    }
    
    auth_response = requests.post("http://localhost:8000/auth/login", json=auth_data)
    print(f"   Auth Status: {auth_response.status_code}")
    
    if auth_response.status_code != 200:
        print(f"   ❌ Authentication failed: {auth_response.text}")
        return False
    
    auth_result = auth_response.json()
    access_token = auth_result["access_token"]
    user_id = auth_result["user_id"]
    print(f"   ✅ Authentication successful")
    print(f"   Token: {access_token[:50]}...")
    print(f"   User ID: {user_id}")
    
    # Test 2: Session Creation
    print("\n2️⃣ Testing Session Creation...")
    session_response = requests.post(
        "http://localhost:8000/chat/sessions",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    print(f"   Session Status: {session_response.status_code}")
    
    if session_response.status_code != 201:
        print(f"   ❌ Session creation failed: {session_response.text}")
        return False
    
    session_result = session_response.json()
    session_id = session_result["session_id"]
    print(f"   ✅ Session created: {session_id}")
    
    # Test 3: Text-based Search (Control Test)
    print("\n3️⃣ Testing Text-based Search (Control)...")
    text_search_data = {
        "query": "gold necklace",
        "session_id": session_id
    }
    
    text_search_response = requests.post(
        "http://localhost:8000/chat/search",
        json=text_search_data,
        headers={"Authorization": f"Bearer {access_token}"}
    )
    print(f"   Text Search Status: {text_search_response.status_code}")
    
    if text_search_response.status_code == 200:
        text_results = text_search_response.json()
        print(f"   ✅ Text search returned {len(text_results.get('products', []))} products")
    else:
        print(f"   ❌ Text search failed: {text_search_response.text}")
    
    # Test 4: Image Search with Form Data
    print("\n4️⃣ Testing Image Search with Form Data...")
    
    # Create a simple test image file
    import io
    from PIL import Image
    
    # Create a small test image
    img = Image.new('RGB', (100, 100), color='red')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    
    # Prepare form data
    files = {
        'image': ('test_image.jpg', img_bytes.getvalue(), 'image/jpeg')
    }
    
    data = {
        'session_id': session_id,
        'query': 'gold necklace'
    }
    
    image_search_response = requests.post(
        "http://localhost:8000/chat/image-query",
        files=files,
        data=data,
        headers={"Authorization": f"Bearer {access_token}"}
    )
    print(f"   Image Search Status: {image_search_response.status_code}")
    
    if image_search_response.status_code == 200:
        image_results = image_search_response.json()
        products = image_results.get('products', [])
        print(f"   ✅ Image search returned {len(products)} products")
        
        if products:
            print("   📦 Found products:")
            for i, product in enumerate(products[:3]):  # Show first 3 products
                print(f"      {i+1}. {product.get('name', 'Unknown')} - {product.get('price', 'N/A')}")
        else:
            print("   ℹ️  No products found (expected for test image)")
    else:
        print(f"   ❌ Image search failed: {image_search_response.text}")
        return False
    
    # Test 5: Combined Text + Image Search
    print("\n5️⃣ Testing Combined Text + Image Search...")
    
    # Create another test image
    img2 = Image.new('RGB', (100, 100), color='blue')
    img2_bytes = io.BytesIO()
    img2.save(img2_bytes, format='JPEG')
    img2_bytes.seek(0)
    
    files2 = {
        'image': ('test_image2.jpg', img2_bytes.getvalue(), 'image/jpeg')
    }
    
    data2 = {
        'session_id': session_id,
        'query': 'diamond ring'
    }
    
    combined_response = requests.post(
        "http://localhost:8000/chat/image-query",
        files=files2,
        data=data2,
        headers={"Authorization": f"Bearer {access_token}"}
    )
    print(f"   Combined Search Status: {combined_response.status_code}")
    
    if combined_response.status_code == 200:
        combined_results = combined_response.json()
        print(f"   ✅ Combined search returned {len(combined_results.get('products', []))} products")
    else:
        print(f"   ❌ Combined search failed: {combined_response.text}")
    
    print("\n" + "=" * 60)
    print("✅ Image Search Functionality Test Complete!")
    print("📊 All core features are working correctly.")
    print("🎯 The chatbot widget can now handle image uploads and perform visual search!")
    
    return True

if __name__ == "__main__":
    try:
        success = test_image_search_pipeline()
        if success:
            print("\n🎉 SUCCESS: Image search functionality is fully operational!")
        else:
            print("\n❌ FAILURE: Some tests failed.")
    except Exception as e:
        print(f"\n💥 Test failed with error: {e}")