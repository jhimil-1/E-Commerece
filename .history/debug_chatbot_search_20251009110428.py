from qdrant_utils import QdrantManager
from clip_utils import clip_manager

# Initialize managers
qdrant = QdrantManager()

# Test the exact same search that chatbot does
query = "laptop"
user_id = "testuser_new"

print(f"Testing search for query: '{query}' with user_id: '{user_id}'")

# Generate embedding (same as chatbot)
query_embedding = clip_manager.get_text_embedding(query)
print(f"Generated embedding dimension: {len(query_embedding)}")

# Search (same as chatbot)
try:
    products = qdrant.search_similar_products(
        query_embedding=query_embedding,
        user_id=user_id,
        limit=5
    )
    
    print(f"Found {len(products)} products")
    
    if products:
        print("\nFirst product details:")
        print(f"Name: '{products[0].get('name', 'MISSING')}'")
        print(f"Category: '{products[0].get('category', 'MISSING')}'")
        print(f"Price: '{products[0].get('price', 'MISSING')}'")
        print(f"Image URL: '{products[0].get('image_url', 'MISSING')}'")
        print(f"Image Path: '{products[0].get('image_path', 'MISSING')}'")
        print(f"Score: {products[0].get('score', 'MISSING')}")
    else:
        print("No products found!")
        
    # Try without user filter
    print("\nTrying search without user filter...")
    products_no_filter = qdrant.search_similar_products(
        query_embedding=query_embedding,
        limit=5
    )
    
    print(f"Found {len(products_no_filter)} products without filter")
    
except Exception as e:
    print(f"Error during search: {e}")
    import traceback
    traceback.print_exc()