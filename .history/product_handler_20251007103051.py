from datetime import datetime
import logging
from typing import List, Dict, Any
from bson import ObjectId
import requests
from database import MongoDB
from gemini_utils import gemini_manager
from qdrant_utils import qdrant_manager
from clip_utils import clip_manager

logger = logging.getLogger(__name__)

class ProductHandler:
    def __init__(self):
        self.db = MongoDB.get_db()
    
    async def process_product_upload(self, products: List[Dict[str, Any]], user_id: str) -> Dict[str, Any]:
        """Process and store uploaded products"""
        try:
            products_to_insert = []
            current_time = datetime.utcnow()
            
            for product in products:
                # Extract fields
                name = product.get("name", "")
                description = product.get("description", "")
                price = product.get("price", 0.0)
                category = product.get("category", "")
                image_data = product.get("image", "")  # Base64 encoded image
                
                # Generate text embedding using CLIP for consistency
                text_content = f"{name} {description} {category}"
                text_embedding = clip_manager.get_text_embedding(text_content)
                
                # Generate image embedding using CLIP if image provided
                image_embedding = None
                if image_data:
                    try:
                        # Handle image URLs from JSON files
                        if image_data.startswith('http'):
                            # Download image from URL
                            import requests
                            response = requests.get(image_data, timeout=10)
                            response.raise_for_status()
                            image_bytes = response.content
                            image_embedding = clip_manager.get_image_embedding(image_bytes)
                        else:
                            # Handle base64 or other formats
                            image_embedding = clip_manager.get_image_embedding(image_data)
                    except Exception as img_error:
                        logger.warning(f"Failed to generate image embedding: {img_error}")
                
                product_doc = {
                    **product,
                    "text_embedding": text_embedding,
                    "image_embedding": image_embedding,
                    "created_at": current_time,
                    "updated_at": current_time,
                    "created_by": user_id,
                    "is_active": True
                }
                products_to_insert.append(product_doc)
            
            # Insert into MongoDB
            if products_to_insert:
                result = self.db.products.insert_many(products_to_insert)
                inserted_ids = [str(id) for id in result.inserted_ids]
                
                # Generate & store embeddings in Qdrant
                await self._generate_and_store_embeddings(products_to_insert, inserted_ids, user_id)
                
                return {
                    "inserted_count": len(inserted_ids),
                    "product_ids": inserted_ids
                }
            
            return {"inserted_count": 0}
        
        except Exception as e:
            logger.error(f"Error in process_product_upload: {str(e)}", exc_info=True)
            raise
    
    async def _generate_and_store_embeddings(self, products: List[Dict[str, Any]], product_ids: List[str], user_id: str):
        """Generate and store vector embeddings for products"""
        try:
            for product, product_id in zip(products, product_ids):
                text = f"{product['name']} {product['description']} {product['category']}"
                
                # Use CLIP embeddings for all products to ensure consistency with Qdrant collection
                embedding = clip_manager.get_text_embedding(text)
                
                qdrant_manager.upsert_product(
                    product_id=product_id,
                    text_embedding=embedding,
                    category=product["category"],
                    metadata={
                        "name": product["name"],
                        "price": product["price"],
                        "created_by": user_id
                    }
                )
        except Exception as e:
            logger.error(f"Error generating/storing embeddings: {str(e)}", exc_info=True)
            pass

    async def search_products(
        self,
        query: str,
        user_id: str,
        session_id: str,
        limit: int = 10,
        category: str = None
    ) -> Dict[str, Any]:
        """Search for products using semantic vector search with category filtering"""
        try:
            # Check if the query is for a specific category
            query_lower = query.lower()
            
            # Common e-commerce categories - removed jewelry-specific restriction
            ecommerce_categories = [
                "electronics", "phones", "laptops", "headphones", "tablets",
                "clothing", "shoes", "accessories", "bags", "watches",
                "home", "furniture", "decor", "kitchen", "appliances",
                "books", "toys", "sports", "fitness", "beauty", "health",
                "jewelry", "necklaces", "earrings", "bracelets", "rings"
            ]
            
            # If no explicit category is provided, try to infer from query
            if not category:
                for cat in ecommerce_categories:
                    if cat in query_lower:
                        category = cat
                        break
            
            # Use CLIP embeddings for better semantic understanding
            query_embedding = clip_manager.get_text_embedding(query)
            
            # Search in Qdrant with user filtering and category filtering
            search_results = qdrant_manager.search_similar_products(
                query_embedding=query_embedding,
                user_id=user_id,
                category_filter=category,
                limit=limit * 2  # Get more results to filter further
            )
            
            if not search_results:
                return {
                    "status": "success",
                    "message": "No products found",
                    "results": []
                }
            
            # Retrieve product documents
            product_ids = [hit["product_id"] for hit in search_results]
            products_cursor = self.db.products.find(
                {"_id": {"$in": [ObjectId(pid) for pid in product_ids]}}
            )
            
            # Create a dictionary to store products by ID
            products_dict = {}
            async for product in products_cursor:
                product_id = str(product["_id"])
                product["_id"] = product_id
                
                # Find the matching search result for this product
                for hit in search_results:
                    if hit["product_id"] == product_id:
                        product["similarity_score"] = hit.get("score", 0.0)
                        # Boost score if category matches
                if category and category.lower() in product.get("category", "").lower():
                    product["similarity_score"] *= 1.2  # Boost score by 20%
                
                # Filter products by user_id to ensure user-specific results
                if product.get("created_by") != user_id:
                    product["similarity_score"] = 0.0  # Hide products from other users
                        break
                
                products_dict[product_id] = product
            
            # Convert to list and sort by boosted score
            products = list(products_dict.values())
            products.sort(key=lambda x: x.get("similarity_score", 0), reverse=True)
            
            # Filter by category if specified
            if category:
                products = [p for p in products if category.lower() in p.get("category", "").lower()]
            
            # Take only the top results
            products = products[:limit]
            
            return {
                "status": "success",
                "query": query,
                "count": len(products),
                "results": products
            }
        
        except Exception as e:
            logger.error(f"Error searching products: {str(e)}", exc_info=True)
            raise

    async def search_jewelry_by_image_and_category(
        self,
        query_text: str = None,
        query_image: str = None,
        category: str = None,
        limit: int = 10,
        min_score: float = 0.1  # Lowered from 0.3 to get more results
    ) -> Dict[str, Any]:
        """
        Search for jewelry using CLIP-based similarity on both image and category.
        
        Args:
            query_text: Text query describing the jewelry
            query_image: Base64 encoded image data
            category: Filter by jewelry category (e.g., 'earrings', 'rings')
            limit: Maximum number of results to return
            min_score: Minimum similarity score (0.0 to 1.0)
            
        Returns:
            Dictionary with search results
        """
        logger.info(f"Starting image search - Category: {category}, Min Score: {min_score}, Has Text: {query_text is not None}, Has Image: {query_image is not None}")
        try:
            # Initialize variables
            text_embedding = None
            image_embedding = None
            
            # Check if we need to extract category from query text
            query_lower = (query_text or "").lower()
            jewelry_categories = ["earrings", "bracelets", "necklaces", "rings", "bangles", "watches"]
            
            # If no explicit category is provided, try to extract from query text
            if not category:
                for cat in jewelry_categories:
                    if cat in query_lower:
                        category = cat  # Set the category to the matched one
                        logger.info(f"Extracted category from query: {category}")
                        break
            
            # Generate text embedding if query_text is provided
            if query_text:
                text_embedding = clip_manager.get_text_embedding(query_text)
            
            # Generate image embedding if query_image is provided
            if query_image:
                image_embedding = clip_manager.get_image_embedding(query_image)
            
            # Determine which embedding to use for search
            if text_embedding is not None and image_embedding is not None:
                # Weighted combination (70% text, 30% image for jewelry)
                search_embedding = [
                    0.7 * t + 0.3 * i
                    for t, i in zip(text_embedding, image_embedding)
                ]
                query_type = "image_and_text"
            elif text_embedding is not None:
                search_embedding = text_embedding
                query_type = "text"
            elif image_embedding is not None:
                search_embedding = image_embedding
                query_type = "image"
            else:
                raise ValueError("Either query_text or query_image must be provided")
            
            # Search in Qdrant with category filter
            logger.info(f"Searching with embedding size: {len(search_embedding)}")
            search_results = qdrant_manager.search_similar(
                query_embedding=search_embedding,
                limit=limit,
                category_filter=category,
                min_score=min_score
            )
            logger.info(f"Raw search results count: {len(search_results)}")
            
            # Log top 3 results for debugging
            for i, result in enumerate(search_results[:3]):
                logger.info(f"Result {i+1} - ID: {result.get('id')}, Score: {result.get('score', 0):.4f}, Category: {result.get('category', 'N/A')}")
            
            # Get product details from MongoDB
            # Use a dictionary to store unique products by their ID
            unique_product_ids = {}
            for hit in search_results:
                product_id = hit["id"]
                # Keep the highest score for each product
                if product_id not in unique_product_ids or hit.get("score", 0) > unique_product_ids[product_id].get("score", 0):
                    unique_product_ids[product_id] = {"id": product_id, "score": hit.get("score", 0)}
            
            if not unique_product_ids:
                return {
                    "status": "success",
                    "message": "No jewelry found matching your criteria",
                    "results": [],
                    "count": 0,
                    "query_type": "image_and_text" if text_embedding and image_embedding else ("text" if text_embedding else "image"),
                    "category_filter": category
                }
            
            # Filter out invalid ObjectIds and get unique product IDs
            valid_ids = []
            for pid in unique_product_ids:
                try:
                    valid_ids.append(ObjectId(pid))
                except:
                    logger.warning(f"Invalid ObjectId: {pid}")
                    continue
            
            if not valid_ids:
                return {
                    "status": "success",
                    "message": "No valid jewelry items found",
                    "results": [],
                    "count": 0,
                    "query_type": "image_and_text" if text_embedding and image_embedding else ("text" if text_embedding else "image"),
                    "category_filter": category
                }
            
            # Get products from MongoDB
            products_cursor = self.db.products.find(
                {"_id": {"$in": valid_ids}}
            )
            
            # Create a list of products with their scores
            products = []
            for product in products_cursor:  # Use regular for loop since it's not async
                product_id = str(product["_id"])
                if product_id in unique_product_ids:
                    product["_id"] = product_id
                    product["similarity_score"] = unique_product_ids[product_id]["score"]
                    products.append(product)
            
            # Sort by score in descending order
            products.sort(key=lambda x: x.get("similarity_score", 0), reverse=True)
            
            # Limit to the requested number of results
            products = products[:limit]
            
            return {
                "status": "success",
                "message": f"Found {len(products)} jewelry items",
                "results": products,
                "count": len(products),
                "query_type": "image_and_text" if text_embedding and image_embedding else ("text" if text_embedding else "image"),
                "category_filter": category
            }
        
        except Exception as e:
            logger.error(f"Error searching jewelry by image and category: {str(e)}", exc_info=True)
            raise


# ✅ Global instance
product_handler = ProductHandler()
