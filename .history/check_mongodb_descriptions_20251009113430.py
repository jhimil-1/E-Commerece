#!/usr/bin/env python3
"""
Check what descriptions are stored in MongoDB
"""

import os
from dotenv import load_dotenv
from database import MongoDB

# Load environment variables
load_dotenv()

def check_mongodb_descriptions():
    """Check what descriptions are stored in MongoDB"""
    try:
        # Get MongoDB connection
        db = MongoDB.get_db()
        
        # Get some sample products
        print("🔍 Checking MongoDB product descriptions:")
        products = db.products.find().limit(10)
        
        for i, product in enumerate(products):
            print(f"\n--- Product {i+1} ---")
            print(f"ID: {product.get('_id')}")
            print(f"Name: {product.get('name', 'N/A')}")
            print(f"Description: {repr(product.get('description', 'MISSING'))}")
            print(f"Category: {product.get('category', 'N/A')}")
            print(f"Price: {product.get('price', 'N/A')}")
            print(f"Image URL: {repr(product.get('image_url', 'MISSING'))}")
            print(f"Image: {repr(product.get('image', 'MISSING'))}")
            
            # Check all keys
            print(f"All keys: {list(product.keys())}")
            
    except Exception as e:
        print(f"❌ Error checking MongoDB: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_mongodb_descriptions()