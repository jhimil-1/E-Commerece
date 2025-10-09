import requests
import json
import base64

# Add some sample jewelry products to the database
def add_jewelry_products():
    base_url = "http://localhost:8000"
    
    # Sample jewelry products
    jewelry_products = [
        {
            "name": "Gold Diamond Ring",
            "description": "Beautiful 14k gold ring with 1 carat diamond",
            "price": 1299.99,
            "category": "Rings",
            "image_url": "https://images.unsplash.com/photo-1602751584552-6ba73aad10e1?w=500",
            "tags": ["gold", "diamond", "ring", "engagement", "wedding"]
        },
        {
            "name": "Silver Pearl Necklace",
            "description": "Elegant sterling silver necklace with freshwater pearls",
            "price": 299.99,
            "category": "Necklaces",
            "image_url": "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=500",
            "tags": ["silver", "pearl", "necklace", "elegant", "freshwater"]
        },
        {
            "name": "Rose Gold Earrings",
            "description": "Stunning rose gold drop earrings with cubic zirconia",
            "price": 199.99,
            "category": "Earrings",
            "image_url": "https://images.unsplash.com/photo-1576053139628-4ba35f3b8c6e?w=500",
            "tags": ["rose gold", "earrings", "cubic zirconia", "drop", "stunning"]
        },
        {
            "name": "White Gold Tennis Bracelet",
            "description": "Classic white gold tennis bracelet with diamonds",
            "price": 899.99,
            "category": "Bracelets",
            "image_url": "https://images.unsplash.com/photo-1618382442787-ed5622384820?w=500",
            "tags": ["white gold", "diamond", "bracelet", "tennis", "classic"]
        },
        {
            "name": "Platinum Wedding Band",
            "description": "Simple and elegant platinum wedding band",
            "price": 799.99,
            "category": "Rings",
            "image_url": "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=500",
            "tags": ["platinum", "wedding", "band", "simple", "elegant"]
        },
        {
            "name": "Gold Chain Necklace",
            "description": "Classic 18k gold chain necklace",
            "price": 449.99,
            "category": "Necklaces",
            "image_url": "https://images.unsplash.com/photo-1603561591411-07134e71a2a9?w=500",
            "tags": ["gold", "chain", "necklace", "classic", "18k"]
        },
        {
            "name": "Diamond Stud Earrings",
            "description": "Timeless diamond stud earrings in white gold",
            "price": 599.99,
            "category": "Earrings",
            "image_url": "https://images.unsplash.com/photo-1602751584552-6ba73aad10e1?w=500",
            "tags": ["diamond", "stud", "earrings", "white gold", "timeless"]
        },
        {
            "name": "Silver Charm Bracelet",
            "description": "Delicate sterling silver charm bracelet",
            "price": 149.99,
            "category": "Bracelets",
            "image_url": "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=500",
            "tags": ["silver", "charm", "bracelet", "delicate", "sterling"]
        }
    ]
    
    print("Adding jewelry products to database...")
    
    for i, product in enumerate(jewelry_products):
        try:
            # Create form data for upload
            form_data = {
                'name': product['name'],
                'description': product['description'],
                'price': str(product['price']),
                'category': product['category'],
                'tags': ','.join(product['tags'])
            }
            
            # Download image and convert to base64
            import urllib.request
            from io import BytesIO
            
            # Get image content
            response = urllib.request.urlopen(product['image_url'])
            image_content = response.read()
            
            # Create multipart form data
            files = {
                'image': ('jewelry_' + str(i) + '.jpg', image_content, 'image/jpeg')
            }
            
            # Make request to add product
            response = requests.post(
                f"{base_url}/products/upload",
                data=form_data,
                files=files
            )
            
            if response.status_code == 200:
                print(f"✅ Added: {product['name']}")
            else:
                print(f"❌ Failed to add {product['name']}: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"❌ Error adding {product['name']}: {str(e)}")
    
    print("\n✨ Jewelry products addition completed!")
    print("You can now search for jewelry terms like:")
    print("- gold ring")
    print("- diamond necklace") 
    print("- silver earrings")
    print("- etc.")

if __name__ == "__main__":
    add_jewelry_products()