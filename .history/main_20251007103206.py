# main.py

# At the very top of main.py
import os
from dotenv import load_dotenv

# Load environment variables first
load_dotenv(override=True)  # Add override=True to ensure it reloads
print("Environment variables loaded:", bool(os.getenv("GOOGLE_API_KEY")))
import json 
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends, status, File, UploadFile, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
import logging
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import uvicorn

# Import auth functions
from auth import (
    get_current_user,
    signup_user,
    login_user,
    create_new_session,
    Token
)

# Import other modules
from database import MongoDB, QdrantManager
from gemini_utils import gemini_manager
from product_handler import product_handler
from chatbot import chatbot_manager
from models import ChatResponse, ChatHistory

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Pydantic models
class UserSignup(BaseModel):
    username: str
    password: str
    email: str

class UserLogin(BaseModel):
    username: str
    password: str

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    category: str
    image_url: str


class ChatQuery(BaseModel):
    query: str
    session_id: str


# Initialize FastAPI app
app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the Jewelry Search API. Visit /docs for API documentation."}

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "ok", "timestamp": datetime.utcnow()}

# Auth endpoints
@app.post("/auth/signup", response_model=dict)
async def signup(user_data: UserSignup):
    try:
        result = await signup_user(
            username=user_data.username,
            password=user_data.password,
            email=user_data.email
        )
        return result
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Signup error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error during signup"
        )

@app.post("/auth/login", response_model=dict)
async def login(user_credentials: UserLogin):
    try:
        return await login_user(
            username=user_credentials.username,
            password=user_credentials.password
        )
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Login error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error during login"
        )

# Session creation endpoint
@app.post("/chat/sessions", response_model=dict, status_code=201)
async def create_session_endpoint(current_user: dict = Depends(get_current_user)):
    """
    Create a new chat session for the authenticated user.
    
    Returns:
        dict: Contains the new session ID and success message
        
    Example Response:
        {
            "session_id": "507f1f77bcf86cd799439011",
            "message": "New chat session created"
        }
    """
    try:
        session_id = await create_new_session(user_id=current_user["username"])
        return {
            "session_id": session_id,
            "message": "New chat session created"
        }
    except Exception as e:
        logger.error(f"Session creation error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating session: " + str(e)
        )
# Add the upload_products endpoint (make sure it's properly indented)
@app.post("/products/upload", response_model=dict)
async def upload_products(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    """
    Upload a JSON file containing product data.
    
    The file should be a JSON array of product objects.
    """
    try:
        # Check file type
        if not file.filename.endswith('.json'):
            raise HTTPException(
                status_code=400,
                detail="Only JSON files are supported"
            )
        
        # Read and validate the file
        contents = await file.read()
        try:
            # Parse JSON content
            products = json.loads(contents)
            # Validate each product matches our schema
            for product in products:
                ProductCreate(**product)
        except ValueError as e:  # Handles both JSONDecodeError and validation errors
            raise HTTPException(
                status_code=400,
                detail=f"Invalid product data: {str(e)}"
            )
        
        # Process the products
        result = await product_handler.process_product_upload(
            products=products,
            user_id=current_user["user_id"]
        )
        
        return {
            "status": "success",
            "message": f"Successfully uploaded {len(products)} products",
            "details": result
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Product upload error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Error processing product upload"
        )
@app.post("/chat/query", response_model=ChatResponse)
async def chat_query(
    chat_data: ChatQuery,
    current_user: dict = Depends(get_current_user)
):
    """
    Process a text-based product search query.
    
    - **query**: Text query describing what you're looking for
    - **session_id**: Active session identifier
    """
    try:
        response = await chatbot_manager.handle_text_query(
            session_id=chat_data.session_id,
            query=chat_data.query
        )
        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Chat query error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Error processing chat query"
        )

@app.post("/chat/image-query", response_model=ChatResponse)
async def image_search(
    session_id: str = Form(...),
    query: Optional[str] = Form(None),
    category: Optional[str] = Form(None),
    image: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    """
    Search for products using an image and optional text query.
    
    - **session_id**: Active session identifier
    - **query**: (Optional) Text query to refine the search
    - **category**: (Optional) Filter by jewelry category (e.g., 'rings', 'earrings')
    - **image**: Upload an image file (JPG, PNG, WEBP)
    """
    try:
        # Validate image file
        allowed_types = ["image/jpeg", "image/png", "image/jpg", "image/webp"]
        if image.content_type not in allowed_types:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid image type. Allowed: {', '.join(allowed_types)}"
            )
        
        # Read image content
        image_bytes = await image.read()
        
        # Log image processing
        logger.info(f"Processing image search - Size: {len(image_bytes)} bytes, Category: {category}")
        
        # Process the image query using product_handler with lower threshold
        search_results = await product_handler.search_jewelry_by_image_and_category(
            query_text=query,
            query_image=image_bytes,
            category=category,
            limit=10,
            min_score=0.1  # Lower threshold for more results
        )
        
        # Log search results
        logger.info(f"Search results count: {search_results.get('count', 0)}")
        if search_results.get('results'):
            logger.info(f"Top result: {search_results['results'][0].get('name', 'N/A')} (Score: {search_results['results'][0].get('similarity_score', 0):.2f})")
        
        # Get current timestamp in ISO format
        from datetime import datetime
        
        # Format the response to match ChatResponse model
        results = search_results.get("results", [])
        response = ChatResponse(
            session_id=session_id,
            query=query or "",
            response=f"Found {len(results)} results matching your image search" + 
                       (f" in category '{category}'" if category else ""),
            products=[{
                "id": str(item["_id"]),
                "name": item.get("name", ""),
                "description": item.get("description", ""),
                "price": str(item.get("price", "")),
                "category": item.get("category", ""),
                "image_url": item.get("image_url", ""),
                "similarity_score": float(item.get("similarity_score", 0.0))
            } for item in results],
            timestamp=datetime.utcnow().isoformat(),
            status="success"
        )
        
        return response
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Image search error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Error processing image search"
        )

# Protected route example
@app.get("/protected-route")
async def protected_route(current_user: dict = Depends(get_current_user)):
    return {"message": f"Hello {current_user['username']}, this is a protected route"}

# Chat history endpoint
@app.get("/chat/history/{session_id}", response_model=ChatHistory)
async def get_chat_history(
    session_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Retrieve chat history for a session.
    
    - **session_id**: Session identifier
    """
    try:
        history = chatbot_manager.get_session_history(session_id)
        return history
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Chat history error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Error retrieving chat history"
        )

# General product similarity search endpoint
@app.post("/products/search", response_model=dict)
async def product_similarity_search(
    query: Optional[str] = Form(None),
    category: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    limit: int = Form(10),
    current_user: dict = Depends(get_current_user)
):
    """
    Search for products using CLIP-based similarity on category and image.
    
    - **query**: (Optional) Text query describing the product
    - **category**: (Optional) Filter by product category (e.g., "electronics", "clothing", "home")
    - **image**: (Optional) Upload an image of product to find similar items
    - **limit**: Maximum number of results to return
    """
    try:
        # Validate inputs
        if not query and not image:
            raise HTTPException(
                status_code=400,
                detail="Either query text or image must be provided"
            )
        
        # Handle image upload if provided
        image_data = None
        if image:
            allowed_types = ["image/jpeg", "image/png", "image/jpg", "image/webp"]
            if image.content_type not in allowed_types:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Invalid image type. Allowed: {', '.join(allowed_types)}"
                )
            
            # Read and convert image to base64
            image_bytes = await image.read()
            import base64
            image_data = base64.b64encode(image_bytes).decode('utf-8')
            
            # Add data URL prefix for CLIP processing
            image_data = f"data:{image.content_type};base64,{image_data}"
        
        # Perform jewelry similarity search
        results = await product_handler.search_jewelry_by_image_and_category(
            query_text=query,
            query_image=image_data,
            category=category,
            limit=limit,
            min_score=0.3
        )
        
        # Return the results directly (already in correct format)
        return results
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Jewelry search error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Error processing jewelry similarity search"
        )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )