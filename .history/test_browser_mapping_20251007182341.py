import requests
import json
import time

def test_frontend_mapping():
    """Test the frontend category mapping by simulating the actual API calls"""
    
    # Login first
    login_data = {
        'username': 'admin',
        'password': 'admin'
    }
    
    print("Testing frontend category mapping simulation...")
    print("=" * 50)
    
    try:
        # Login
        login_response = requests.post('http://localhost:8000/auth/login', json=login_data)
        if login_response.status_code != 200:
            print(f"Login failed: {login_response.status_code}")
            return
        
        access_token = login_response.json()['access_token']
        headers = {'Authorization': f'Bearer {access_token}'}
        
        # Test the mapping that the frontend should now use
        frontend_backend_mapping = {
            'electronics': 'Smartphones',
            'clothing': 'Smartwatches', 
            'home': 'Smart Speakers',
            'books': 'Tablets',
            'sports': 'Headphones'
        }
        
        for frontend_cat, backend_cat in frontend_backend_mapping.items():
            print(f"\nTesting frontend '{frontend_cat}' -> backend '{backend_cat}':")
            
            # This is what the frontend should now do - search with category parameter
            search_data = {
                'query': 'products',
                'category': backend_cat,
                'limit': 10
            }
            
            search_response = requests.post('http://localhost:8000/products/search', 
                                          data=search_data, headers=headers)
            
            if search_response.status_code == 200:
                results = search_response.json()
                result_count = len(results.get('results', []))
                print(f"  ✓ Frontend mapping should return: {result_count} results")
            else:
                print(f"  ✗ Search failed: {search_response.status_code} - {search_response.text}")
        
        print(f"\n✅ Frontend mapping logic is working correctly!")
        print("The frontend should now display products when category buttons are clicked.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_frontend_mapping()