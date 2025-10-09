#!/usr/bin/env python3
"""
Test script to verify the /chat/query endpoint response format
"""

import requests
import json

def test_chat_query():
    """Test the chat query endpoint to see the actual response format"""
    
    # First, let's try to get a session (we'll need to handle auth)
    try:
        # Try without auth first to see what error we get
        print("Testing /chat/query endpoint...")
        
        # Test data
        test_data = {
            "query": "phone",
            "session_id": "test-session-123",
            "limit": 5
        }
        
        response = requests.post(
            'http://localhost:8000/chat/query',
            json=test_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 401:
            print("Got 401 Unauthorized - this is expected without auth token")
            print("Let's check what the response structure should be...")
            
            # Let's check the ChatResponse model to understand the expected format
            print("\nChecking ChatResponse model structure...")
            
            # Read the models file to understand the expected format
            try:
                with open('models.py', 'r') as f:
                    content = f.read()
                    # Look for ChatResponse class
                    if 'class ChatResponse' in content:
                        lines = content.split('\n')
                        in_class = False
                        for line in lines:
                            if 'class ChatResponse' in line:
                                in_class = True
                                print(f"Found ChatResponse: {line.strip()}")
                            elif in_class and line.strip().startswith('class '):
                                break
                            elif in_class and line.strip():
                                print(f"  {line.strip()}")
            except Exception as e:
                print(f"Could not read models.py: {e}")
                
        else:
            data = response.json()
            print(f"Response keys: {list(data.keys())}")
            
            if 'products' in data:
                print(f"Found products field with {len(data['products'])} items")
                if data['products']:
                    print(f"First product keys: {list(data['products'][0].keys())}")
            elif 'results' in data:
                print(f"Found results field with {len(data['results'])} items")
            else:
                print(f"Available keys: {list(data.keys())}")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_chat_query()