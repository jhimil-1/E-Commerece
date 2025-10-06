# qdrant_utils.py
# gemini_utils.py
import os
from dotenv import load_dotenv
load_dotenv()  # 
import logging
from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.exceptions import UnexpectedResponse

from config import (
    QDRANT_URL,
    QDRANT_API_KEY,
    QDRANT_COLLECTION_NAME
)

logger = logging.getLogger(__name__)

class QdrantManager:
    """Manager for Qdrant vector database operations"""
    
    def __init__(self):
        """Initialize Qdrant client"""
        self.client = QdrantClient(
            url=QDRANT_URL,
            api_key=QDRANT_API_KEY
        )
        self.collection_name = QDRANT_COLLECTION_NAME
        self._ensure_collection_exists()
    
    def _ensure_collection_exists(self, vector_size: int = 512):
        """Ensure the collection exists, create if it doesn't"""
        try:
            collections = self.client.get_collections()
            collection_names = [collection.name for collection in collections.collections]
            
            if self.collection_name not in collection_names:
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(
                        size=vector_size,
                        distance=models.Distance.COSINE
                    )
                )
                logger.info(f"Created collection: {self.collection_name}")
            else:
                # Check if existing collection has correct vector size
                collection_info = self.client.get_collection(self.collection_name)
                existing_size = collection_info.config.params.vectors.size
                if existing_size != vector_size:
                    logger.warning(f"Collection {self.collection_name} has wrong vector size {existing_size}, expected {vector_size}. Recreating collection...")
                    self.client.delete_collection(self.collection_name)
                    self.client.create_collection(
                        collection_name=self.collection_name,
                        vectors_config=models.VectorParams(
                            size=vector_size,
                            distance=models.Distance.COSINE
                        )
                    )
                    logger.info(f"Recreated collection: {self.collection_name} with correct vector size")
                else:
                    logger.info(f"Using existing collection: {self.collection_name}")
                
        except UnexpectedResponse as e:
            logger.error(f"Error creating Qdrant collection: {e}")
            raise
    
    def recreate_collection(self, vector_size: int = 512):
        """Recreate the collection with the specified vector size"""
        try:
            # Delete existing collection if it exists
            try:
                self.client.delete_collection(self.collection_name)
                logger.info(f"Deleted existing collection: {self.collection_name}")
            except Exception:
                # Collection might not exist, which is fine
                pass
            
            # Create new collection
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=vector_size,
                    distance=models.Distance.COSINE
                )
            )
            logger.info(f"Created collection: {self.collection_name} with vector size {vector_size}")
            
        except Exception as e:
            logger.error(f"Error recreating collection: {e}")
            raise
    
    def search_similar(
        self,
        query_embedding: List[float],
        limit: int = 10,
        category_filter: Optional[str] = None,
        min_score: float = 0.0
    ) -> List[Dict[str, Any]]:
        """Search for similar vectors in Qdrant with optional category filtering"""
        try:
            # Build filter query if category is specified
            query_filter = None
            if category_filter:
                # Create payload index for category if it doesn't exist
                try:
                    self.client.create_payload_index(
                        collection_name=self.collection_name,
                        field_name="category",
                        field_schema=models.PayloadSchemaType.KEYWORD
                    )
                except Exception:
                    # Index might already exist, which is fine
                    pass
                
                # Try exact match first, then fallback to case-insensitive match
                query_filter = models.Filter(
                    must=[
                        models.FieldCondition(
                            key="category",
                            match=models.MatchValue(value=category_filter)
                        )
                    ]
                )
            
            # Try search with exact category match first
            search_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                query_filter=query_filter,
                limit=limit,
                score_threshold=min_score
            )
            
            # If no results and category filter is applied, try case-insensitive variations
            if not search_results and category_filter:
                # Try different case variations
                case_variations = [
                    category_filter.capitalize(),  # rings -> Rings
                    category_filter.lower(),       # RINGS -> rings
                    category_filter.upper()        # rings -> RINGS
                ]
                
                for variation in case_variations:
                    if variation == category_filter:
                        continue  # Skip if same as original
                    
                    alt_filter = models.Filter(
                        must=[
                            models.FieldCondition(
                                key="category",
                                match=models.MatchValue(value=variation)
                            )
                        ]
                    )
                    
                    search_results = self.client.search(
                        collection_name=self.collection_name,
                        query_vector=query_embedding,
                        query_filter=alt_filter,
                        limit=limit,
                        score_threshold=min_score
                    )
                    
                    if search_results:
                        logger.info(f"Found results using case variation: {variation}")
                        break
            
            return [
                {
                    "id": hit.payload.get("mongo_id", str(hit.id)),  # Return original MongoDB ID if available
                    "score": hit.score,
                    "payload": hit.payload
                }
                for hit in search_results
            ]
        except Exception as e:
            logger.error(f"Error searching in Qdrant: {str(e)}")
            # Return empty results instead of raising
            return []
    
    def search_similar_products(
        self, 
        query_embedding: List[float], 
        user_id: Optional[str] = None,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Search for similar products using vector similarity with user filtering
        
        Args:
            query_embedding: Query vector embedding
            user_id: Optional user ID to filter results (username)
            limit: Maximum number of results
            
        Returns:
            List of similar products with scores
        """
        try:
            # Build filter for user-specific search
            query_filter = None
            if user_id:
                # Create payload index for created_by if it doesn't exist
                try:
                    self.client.create_payload_index(
                        collection_name=self.collection_name,
                        field_name="created_by",
                        field_schema=models.PayloadSchemaType.KEYWORD
                    )
                except Exception:
                    # Index might already exist, which is fine
                    pass
                
                query_filter = models.Filter(
                    must=[
                        models.FieldCondition(
                            key="created_by",
                            match=models.MatchValue(value=user_id)
                        )
                    ]
                )
            
            # Perform similarity search
            search_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                query_filter=query_filter,
                limit=limit
            )
            
            # Format results
            products = []
            for result in search_results:
                product = {
                    "product_id": result.payload.get("mongo_id", str(result.id)),
                    "name": result.payload.get("name", ""),
                    "category": result.payload.get("category", ""),
                    "price": result.payload.get("price", 0.0),
                    "description": result.payload.get("description", ""),
                    "score": result.score
                }
                products.append(product)
            
            logger.info(f"Found {len(products)} similar products for user {user_id}")
            return products
        
        except Exception as e:
            logger.error(f"Error searching products: {str(e)}")
            return []
    
    def upsert_product(
        self,
        product_id: str,
        text_embedding: List[float],
        image_embedding: Optional[List[float]] = None,
        category: Optional[str] = None,
        metadata: Dict[str, Any] = None
    ) -> bool:
        """Upsert product vector into Qdrant with optional image embedding"""
        try:
            # Convert MongoDB ObjectId string to integer hash for Qdrant point ID
            import hashlib
            point_id = int(hashlib.md5(product_id.encode()).hexdigest(), 16) % (10**18)
            
            # Prepare payload with original MongoDB ID and category
            payload = metadata or {}
            payload["mongo_id"] = product_id
            if category:
                payload["category"] = category
            
            # Use text embedding as primary vector, or combine with image if available
            if image_embedding and text_embedding:
                # Combine text and image embeddings (weighted average)
                combined_vector = [
                    0.7 * t + 0.3 * i 
                    for t, i in zip(text_embedding, image_embedding)
                ]
                vector = combined_vector
            else:
                vector = text_embedding
            
            # Create point
            point = models.PointStruct(
                id=point_id,
                vector=vector,
                payload=payload
            )
            
            # Upsert the point
            operation_info = self.client.upsert(
                collection_name=self.collection_name,
                points=[point]
            )
            
            logger.info(f"Product upserted successfully: {product_id} (category: {category})")
            return True
            
        except Exception as e:
            logger.error(f"Error upserting product {product_id}: {str(e)}")
            return False


# Initialize a global instance
qdrant_manager = QdrantManager()
