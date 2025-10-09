from qdrant_utils import QdrantManager

qdrant = QdrantManager()

# Check collection info
try:
    collection_info = qdrant.client.get_collection(qdrant.collection_name)
    print(f"Collection: {qdrant.collection_name}")
    print(f"Vector size: {collection_info.config.params.vectors.size}")
    print(f"Points count: {collection_info.points_count}")
    print(f"Status: {collection_info.status}")
except Exception as e:
    print(f"Error getting collection info: {e}")
    import traceback
    traceback.print_exc()