from qdrant_utils import QdrantManager
from config import QDRANT_COLLECTION_NAME

def test_qdrant():
    print(f"QDRANT_COLLECTION_NAME: {QDRANT_COLLECTION_NAME}")
    
    try:
        qdrant = QdrantManager()
        print("QdrantManager initialized successfully")
        
        # Try to get collection info
        try:
            info = qdrant.client.get_collection(QDRANT_COLLECTION_NAME)
            print(f"Collection exists: {QDRANT_COLLECTION_NAME}")
            print(f"Points count: {info.points_count}")
        except Exception as e:
            print(f"Collection error: {e}")
            
    except Exception as e:
        print(f"QdrantManager initialization error: {e}")

if __name__ == "__main__":
    test_qdrant()