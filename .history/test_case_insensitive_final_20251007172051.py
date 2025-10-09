import requests

def test_case_insensitive_search():
    """Test that category search works regardless of case"""
    
    # Login first
    login_data = {
        "username": "test_user2",
        "password": "test123"
    }
    
    response = requests.post("http://localhost:8000/auth/login", json=login_data)
    if response.status_code != 200:
        print(f"❌ Login failed: {response.status_code} - {response.text}")
        return False
    
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test cases: (query, category, expected_count)
    test_cases = [
        # Original working cases (capitalized)
        ("Laptops", "Laptops", 10),
        ("Headphones", "Headphones", 10),
        ("Smartphones", "Smartphones", 8),
        
        # Lowercase cases (should now work)
        ("laptops", "laptops", 10),
        ("headphones", "headphones", 10),
        ("smartphones", "smartphones", 8),
        
        # Mixed case cases (should now work)
        ("LapTopS", "LapTopS", 10),
        ("HeAdPhOnEs", "HeAdPhOnEs", 10),
        ("SmArTpHoNeS", "SmArTpHoNeS", 8),
        
        # Uppercase cases (should now work)
        ("LAPTOPS", "LAPTOPS", 10),
        ("HEADPHONES", "HEADPHONES", 10),
        ("SMARTPHONES", "SMARTPHONES", 8),
        
        # Non-existent category (should return 0)
        ("electronics", "electronics", 0),
        ("ELECTRONICS", "ELECTRONICS", 0),
    ]
    
    all_passed = True
    
    for query, category, expected_count in test_cases:
        form_data = {
            "query": query,
            "category": category,
            "limit": 20
        }
        
        response = requests.post(
            "http://localhost:8000/products/search",
            data=form_data,
            headers=headers
        )
        
        if response.status_code == 200:
            result = response.json()
            actual_count = result.get('count', 0)
            
            if actual_count == expected_count:
                status = "✅ PASS"
            else:
                status = "❌ FAIL"
                all_passed = False
            
            print(f"{status} '{category}' -> Expected: {expected_count}, Got: {actual_count}")
            
            if actual_count > 0 and actual_count == expected_count:
                first_result = result.get('results', [])[0]
                print(f"    First result: {first_result.get('name')} (category: '{first_result.get('category')}')")
        else:
            print(f"❌ FAIL '{category}' -> HTTP {response.status_code}: {response.text}")
            all_passed = False
    
    print(f"\n{'='*50}")
    if all_passed:
        print("🎉 ALL TESTS PASSED! Case-insensitive search is working correctly.")
    else:
        print("❌ Some tests failed. Case-insensitive search needs more work.")
    
    return all_passed

if __name__ == "__main__":
    test_case_insensitive_search()