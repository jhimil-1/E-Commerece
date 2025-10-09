from qdrant_utils import QdrantManager
from config import QDRANT_COLLECTION_NAME

def check_qdrant_payload():
    qdrant = QdrantManager()
    
    # Get a few points from Qdrant
    try:
        # Scroll through collection to get some points
        scroll_result = qdrant.client.scroll(
            collection_name=QDRANT_COLLECTION_NAME,
            limit=3,
            with_payload=True,
            with_vectors=False
        )
        
        points = scroll_result[0]  # First element is the list of points
        print(f"Found {len(points)} points in Qdrant:")
        
        for i, point in enumerate(points):
            print(f"\nPoint {i+1} (ID: {point.id}):")
            print(f"  Payload: {point.payload}")
            
    except Exception as e:
        print(f"Error scrolling collection: {e}")

if __name__ == "__main__":
    check_qdrant_payload()