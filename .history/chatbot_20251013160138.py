"""
Chatbot logic for handling text and image queries
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
from PIL import Image
import io
import logging

from database import MongoDB
from qdrant_utils import qdrant_manager
from gemini_utils import gemini_manager
from clip_utils import clip_manager
from models import ChatResponse, ChatHistoryItem, ChatHistory
from product_handler import ProductHandler

logger = logging.getLogger(__name__)


class ChatbotManager:
    """Manager for chatbot operations"""
    
    MAX_HISTORY_LENGTH = 10
    
    def __init__(self):
        """Initialize chatbot manager"""
        self.chat_collection = MongoDB.get_collection("chat_history")
        self.sessions_collection = MongoDB.get_collection("sessions")
        self.products_collection = MongoDB.get_collection("products")
        self.product_handler = ProductHandler()
    
    def _get_chat_history(self, session_id: str) -> List[Dict[str, str]]:
        """
        Retrieve chat history for a session
        
        Args:
            session_id: Session identifier
            
        Returns:
            List of chat messages
        """
        messages = list(
            self.chat_collection.find(
                {"session_id": session_id}
            ).sort("timestamp", -1).limit(self.MAX_HISTORY_LENGTH)
        )
        
        # Reverse to get chronological order
        messages.reverse()
        
        return [
            {
                "role": msg["role"],
                "content": msg["content"]
            }
            for msg in messages
        ]
    
    def _save_chat_message(
        self, 
        session_id: str, 
        role: str, 
        content: str, 
        products: Optional[List[Dict]] = None
    ):
        """
        Save a chat message to history
        
        Args:
            session_id: Session identifier
            role: Message role (user/assistant)
            content: Message content
            products: Optional product list
        """
        message_doc = {
            "session_id": session_id,
            "role": role,
            "content": content,
            "products": products or [],
            "timestamp": datetime.utcnow()
        }
        
        self.chat_collection.insert_one(message_doc)
        
        # Update session last activity
        self.sessions_collection.update_one(
            {"session_id": session_id},
            {"$set": {"last_activity": datetime.utcnow()}}
        )
        
        # Maintain max history length
        message_count = self.chat_collection.count_documents({"session_id": session_id})
        if message_count > self.MAX_HISTORY_LENGTH:
            # Delete oldest messages
            oldest_messages = list(
                self.chat_collection.find(
                    {"session_id": session_id}
                ).sort("timestamp", 1).limit(message_count - self.MAX_HISTORY_LENGTH)
            )
            
            message_ids = [msg["_id"] for msg in oldest_messages]
            self.chat_collection.delete_many({"_id": {"$in": message_ids}})
    
    def _verify_session(self, session_id: str) -> bool:
        """Verify that a session exists and is valid"""
        if not session_id:
            logger.warning("Empty session ID provided")
            return False
            
        session = self.sessions_collection.find_one({"session_id": session_id})
        if not session:
            logger.warning(f"No session found with ID: {session_id}")
            return False
            
        # Optional: Add additional session validation here
        # For example, check if session is expired
        return True
        
    def _get_user_from_session(self, session_id: str) -> Optional[str]:
        """Get user_id from session_id"""
        if not session_id:
            logger.warning("Empty session ID provided")
            return None
            
        session = self.sessions_collection.find_one({"session_id": session_id})
        if not session:
            logger.warning(f"No session found with ID: {session_id}")
            # Debug: Check all sessions
            all_sessions = list(self.sessions_collection.find({}).limit(5))
            logger.info(f"Available sessions: {[str(s.get('session_id', 'no-id')) for s in all_sessions]}")
            return None
            
        user_id = session.get("user_id")
        logger.info(f"Found user_id: {user_id} for session: {session_id}")
        return user_id
        
    def _enrich_products_with_mongodb(self, products: List[Dict]) -> List[Dict]:
        """
        Enrich products with full data from MongoDB
        
        Args:
            products: List of products from Qdrant search
            
        Returns:
            List of products with enriched data from MongoDB
        """
        if not products:
            return products
            
        enriched_products = []
        
        for product in products:
            try:
                # Get the MongoDB product ID from the Qdrant result
                product_id = product.get("product_id")
                if not product_id:
                    logger.warning(f"No product_id found in Qdrant result: {product}")
                    enriched_products.append(product)
                    continue
                
                # Convert to ObjectId if it's a valid ObjectId string
                from bson import ObjectId
                try:
                    if len(product_id) == 24:  # Valid ObjectId length
                        mongo_product_id = ObjectId(product_id)
                    else:
                        mongo_product_id = product_id
                except:
                    mongo_product_id = product_id
                
                # Fetch the full product document from MongoDB
                mongo_product = self.products_collection.find_one({"_id": mongo_product_id})
                
                if mongo_product:
                    # Merge Qdrant data with MongoDB data, prioritizing MongoDB for description
                    enriched_product = {
                        "product_id": product_id,
                        "name": product.get("name", mongo_product.get("name", "")),
                        "category": product.get("category", mongo_product.get("category", "")),
                        "price": product.get("price", mongo_product.get("price", 0.0)),
                        "description": mongo_product.get("description", ""),  # Use MongoDB description
                        "score": product.get("score", 0.0),
                        "image_url": product.get("image_url", mongo_product.get("image_url", "")),
                        "image_path": product.get("image_path", mongo_product.get("image_path", "")),
                        "image": product.get("image", mongo_product.get("image", "")),
                        "payload": product.get("payload", {})
                    }
                    
                    # Add any additional fields from MongoDB
                    for field in ["in_stock", "created_at", "created_by"]:
                        if field in mongo_product:
                            enriched_product[field] = mongo_product[field]
                    
                    enriched_products.append(enriched_product)
                    logger.debug(f"Enriched product {product_id} with MongoDB data")
                else:
                    logger.warning(f"No MongoDB product found for ID: {product_id}")
                    enriched_products.append(product)
                    
            except Exception as e:
                logger.error(f"Error enriching product {product.get('product_id', 'unknown')}: {str(e)}")
                enriched_products.append(product)  # Fall back to original product
        
        return enriched_products
    async def handle_text_query(
        self, 
        session_id: str, 
        query: str,
        category: Optional[str] = None,
        limit: int = 5
    ) -> ChatResponse:
        """
        Handle text-based query
        
        Args:
            session_id: Session identifier
            query: User's text query
            
        Returns:
            Chat response with products
        """
        try:
            logger.info(f"Processing text query for session: {session_id}")
            
            # Verify session
            logger.info(f"Verifying session: {session_id}")
            if not self._verify_session(session_id):
                logger.error(f"Invalid session ID: {session_id}")
                raise ValueError("Invalid session ID")
            
            # Get user ID for filtering
            logger.info(f"Getting user from session: {session_id}")
            user_id = self._get_user_from_session(session_id)
            if not user_id:
                logger.error(f"No user found for session: {session_id}")
                raise ValueError("Invalid user session")
            
            logger.info(f"Found user ID: {user_id} for session: {session_id}")
            
            # Save user message
            logger.debug(f"Saving user message: {query}")
            self._save_chat_message(session_id, "user", query)
            
            # Get query embedding
            logger.debug("Generating query embedding...")
            try:
                # Use CLIP for text embedding to match product embeddings
                query_embedding = clip_manager.get_text_embedding(query)
                if not query_embedding:
                    raise ValueError("Failed to generate query embedding")
                logger.debug("Successfully generated query embedding")
            except Exception as e:
                logger.error(f"Error generating query embedding: {str(e)}")
                raise ValueError("Failed to process your query. Please try again.")
            
            # Search for similar products
            logger.debug("Searching for similar products...")
            try:
                # Use product handler for proper category filtering
                logger.info(f"Calling product_handler.search_products with query='{query}', user_id='{user_id}', category='{category}', limit={limit}")
                search_result = await self.product_handler.search_products(
                    query=query,
                    query_embedding=query_embedding,
                    user_id=user_id,
                    category=category,
                    limit=limit
                )
                
                logger.info(f"Product handler returned: {search_result}")
                if search_result['status'] == 'success':
                    products = search_result['results']
                    logger.info(f"Found {len(products)} similar products from product handler")
                else:
                    logger.error(f"Product search failed: {search_result['message']}")
                    products = []
                
            except Exception as e:
                logger.error(f"Error searching products: {str(e)}")
                # Fallback to direct Qdrant search if product handler fails
                try:
                    products = qdrant_manager.search_similar_products(
                        query_embedding=query_embedding,
                        user_id=user_id,
                        category_filter=category,
                        limit=limit
                    )
                    products = self._enrich_products_with_mongodb(products)
                    logger.info(f"Fallback: Found {len(products)} products from direct Qdrant search")
                except Exception as fallback_error:
                    logger.error(f"Fallback search also failed: {str(fallback_error)}")
                    products = []  # Continue with empty product list
            
            # Get chat history
            chat_history = self._get_chat_history(session_id)
            
            # Generate natural language response
            logger.debug("Generating response...")
            try:
                response_text = gemini_manager.generate_response(
                    query=query,
                    products=products,
                    chat_history=chat_history
                )
            except Exception as e:
                logger.error(f"Error generating response: {str(e)}")
                response_text = "I'm sorry, I encountered an error processing your request. Please try again."
            
            # Save assistant response
            self._save_chat_message(session_id, "assistant", response_text, products)
            
            response = ChatResponse(
                session_id=session_id,
                query=query,
                response=response_text,
                products=products,
                timestamp=datetime.utcnow()
            )
            
            logger.info(f"Successfully processed query for session: {session_id}")
            return response
        
        except ValueError as e:
            logger.error(f"Validation error in handle_text_query: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in handle_text_query: {str(e)}", exc_info=True)
            raise
    
    async def handle_image_query(
        self, 
        session_id: str, 
        query: str, 
        image_bytes: bytes
    ) -> ChatResponse:
        """
        Handle image-based query
        
        Args:
            session_id: Session identifier
            query: User's text query accompanying the image
            image_bytes: Image file bytes
            
        Returns:
            Chat response with products
        """
        try:
            # Verify session
            if not self._verify_session(session_id):
                raise ValueError("Invalid session ID")
            
            # Get user ID for filtering
            user_id = self._get_user_from_session(session_id)
            
            # Open image
            image = Image.open(io.BytesIO(image_bytes))
            
            # Save user message
            user_message = f"{query} [Image uploaded]"
            self._save_chat_message(session_id, "user", user_message)
            
            # Get query embedding using CLIP for image and text
            text_embedding = clip_manager.get_text_embedding(query)
            image_embedding = clip_manager.get_image_embedding(image)
            
            # Combine embeddings (70% text, 30% image for jewelry)
            query_embedding = [
                0.7 * t + 0.3 * i
                for t, i in zip(text_embedding, image_embedding)
            ]
            
            # Search for similar products
            products = qdrant_manager.search_similar_products(
                query_embedding=query_embedding,
                user_id=user_id,
                limit=5
            )
            
            # Enrich products with MongoDB data (descriptions, full image URLs, etc.)
            products = self._enrich_products_with_mongodb(products)
            
            # Get chat history
            chat_history = self._get_chat_history(session_id)
            
            # Generate natural language response
            response_text = gemini_manager.generate_response(
                query=f"{query} (based on uploaded image)",
                products=products,
                chat_history=chat_history
            )
            
            # Save assistant response
            self._save_chat_message(session_id, "assistant", response_text, products)
            
            return ChatResponse(
                session_id=session_id,
                query=user_message,
                response=response_text,
                products=products,
                timestamp=datetime.utcnow()
            )
        
        except Exception as e:
            logger.error(f"Error handling image query: {e}")
            raise
    
    def get_session_history(self, session_id: str) -> ChatHistory:
        """
        Retrieve complete chat history for a session
        
        Args:
            session_id: Session identifier
            
        Returns:
            Chat history with all messages
        """
        try:
            # Verify session
            if not self._verify_session(session_id):
                raise ValueError("Invalid session ID")
            
            # Get all messages
            messages_cursor = self.chat_collection.find(
                {"session_id": session_id}
            ).sort("timestamp", 1)
            
            messages = []
            for msg in messages_cursor:
                messages.append(
                    ChatHistoryItem(
                        role=msg["role"],
                        content=msg["content"],
                        products=msg.get("products"),
                        timestamp=msg["timestamp"]
                    )
                )
            
            return ChatHistory(
                session_id=session_id,
                messages=messages
            )
        
        except Exception as e:
            logger.error(f"Error retrieving chat history: {e}")
            raise


# Global chatbot manager instance
chatbot_manager = ChatbotManager()