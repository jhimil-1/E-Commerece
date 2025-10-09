from database import MongoDB

# Check what fields are available in products
db = MongoDB.get_db()
products = list(db.products.find().limit(3))
for i, product in enumerate(products):
    print(f'Product {i+1}:')
    print(f'  Name: {product.get("name", "N/A")}')
    image_fields = [k for k in product.keys() if 'image' in k.lower()]
    print(f'  Image fields: {image_fields}')
    for key in image_fields:
        print(f'  {key}: {product[key]}')
    print()