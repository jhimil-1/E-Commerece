# clear_products.py
from database import MongoDB, qdrant_manager
from config import QDRANT_COLLECTION_NAME

def clear_all_products():
    # Clear MongoDB products
    db = MongoDB.get_db()
    products_deleted = db.products.delete_many({}).deleted_count
    print(f"Deleted {products_deleted} products from MongoDB")
    
    # Clear Qdrant collection
    try:
        qdrant_manager.get_client().delete_collection(collection_name=QDRANT_COLLECTION_NAME)
        print(f"Deleted Qdrant collection: {QDRANT_COLLECTION_NAME}")
    except Exception as e:
        print(f"Error deleting Qdrant collection: {e}")
    
    print("All products and vector data have been cleared.")

if __name__ == "__main__":
    clear_all_products()
