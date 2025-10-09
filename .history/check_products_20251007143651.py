#!/usr/bin/env python3
"""
Script to check current products in the database
"""

from database import MongoDB

def check_products():
    """Check current products in database"""
    try:
        db = MongoDB.get_db()
        
        # Get total count
        total_count = db.products.count_documents({})
        print(f"📊 Total products in database: {total_count}")
        
        # Get recent products
        recent_products = list(db.products.find().sort("created_at", -1).limit(10))
        
        if recent_products:
            print("\n📋 Recent products:")
            for i, product in enumerate(recent_products, 1):
                name = product.get("name", "No name")
                category = product.get("category", "No category")
                created_by = product.get("created_by", "Unknown")
                created_at = product.get("created_at", "No date")
                print(f"{i}. {name} | Category: {category} | Created by: {created_by} | Date: {created_at}")
        else:
            print("\n❌ No products found in database")
            
        # Check by category
        categories = db.products.distinct("category")
        if categories:
            print(f"\n🏷️  Categories found: {', '.join(categories)}")
            
            for category in categories:
                count = db.products.count_documents({"category": category})
                print(f"   {category}: {count} products")
        
    except Exception as e:
        print(f"❌ Error checking products: {e}")

if __name__ == "__main__":
    check_products()