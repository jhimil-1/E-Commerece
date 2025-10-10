import requests
import json
import sys

def test_business_dress_search():
    """Test search for 'Business Professional Dress' to verify category filtering works"""
    
    # Get fresh token
    login_response = requests.post('http://localhost:8000/auth/login', json={
        'username': 'test_user_02ff81cd',
        'password': 'test_password'
    })
    
    if login_response.status_code != 200:
        print(f"Login failed: {login_response.status_code} - {login_response.text}")
        return False
    
    token = login_response.json()['access_token']
    
    # Create session
    session_response = requests.post('http://localhost:8000/chat/sessions', 
                                   headers={'Authorization': f'Bearer {token}'})
    
    if session_response.status_code != 201:
        print(f"Session creation failed: {session_response.status_code} - {session_response.text}")
        return False
    
    session_id = session_response.json()['session_id']
    
    # Test search without category filter (should return mixed results)
    print("Testing search without category filter...")
    response1 = requests.post('http://localhost:8000/chat/query', 
                             headers={'Authorization': f'Bearer {token}'},
                             json={
                                 'query': 'Business Professional Dress',
                                 'session_id': session_id,
                                 'limit': 10
                             })
    
    if response1.status_code == 200:
        results1 = response1.json()
        print(f"Found {len(results1['products'])} products without category filter:")
        for product in results1['products']:
            print(f"  - {product['name']} ({product['category']}) - Score: {product.get('similarity_score', 'N/A')}")
    else:
        print(f"Search failed: {response1.status_code} - {response1.text}")
        return False
    
    # Test search with clothing category filter (should return only clothing)
    print("\nTesting search with clothing category filter...")
    response2 = requests.post('http://localhost:8000/chat/query', 
                             headers={'Authorization': f'Bearer {token}'},
                             json={
                                 'query': 'Business Professional Dress',
                                 'session_id': session_id,
                                 'category': 'clothing',
                                 'limit': 10
                             })
    
    if response2.status_code == 200:
        results2 = response2.json()
        print(f"Found {len(results2['products'])} products with clothing category filter:")
        for product in results2['products']:
            print(f"  - {product['name']} ({product['category']}) - Score: {product.get('similarity_score', 'N/A')}")
        
        # Check if all results are clothing
        non_clothing = [p for p in results2['products'] if p['category'].lower() != 'clothing']
        if non_clothing:
            print(f"ERROR: Found {len(non_clothing)} non-clothing items in filtered search!")
            for product in non_clothing:
                print(f"  - {product['name']} ({product['category']})")
            return False
        else:
            print("SUCCESS: All results are clothing items!")
            return True
    else:
        print(f"Search with category filter failed: {response2.status_code} - {response2.text}")
        return False

if __name__ == "__main__":
    success = test_business_dress_search()
    sys.exit(0 if success else 1)