#!/usr/bin/env python3
"""
Simple test server to simulate the race condition scenario
"""
from flask import Flask, jsonify, request
import time
import random

app = Flask(__name__)

# Simulate some chat history with potential sync issues
chat_history = [
    {
        "role": "user",
        "content": "show me necklaces",
        "products": None
    },
    {
        "role": "assistant", 
        "content": "Absolutely! Switching over to necklaces for you. I found a beautiful Pearl Strand Necklace for $399.99. It's an elegant 18-inch strand of AAA-grade freshwater pearls with a lovely gold clasp.",
        "products": [
            {"name": "Pearl Strand Necklace", "price": 399.99, "description": "Elegant 18-inch strand of AAA-grade freshwater pearls with gold clasp."}
        ]
    }
]

# Current products that might be out of sync
current_products = [
    {"name": "Men's Chronograph Watch", "price": 699.99, "description": "Stainless steel chronograph watch with sapphire crystal and leather strap.", "category": "watch"},
    {"name": "Pearl Strand Necklace", "price": 399.99, "description": "Elegant 18-inch strand of AAA-grade freshwater pearls with gold clasp.", "category": "necklace"},
    {"name": "Rose Gold Watch", "price": 449.99, "description": "Elegant rose gold-plated watch with mother-of-pearl dial and leather band.", "category": "watch"},
    {"name": "Platinum Wedding Band", "price": 599.99, "description": "Classic 4mm platinum wedding band with polished finish.", "category": "ring"},
    {"name": "Silver Charm Bracelet", "price": 129.99, "description": "Sterling silver charm bracelet with 5 interchangeable charms included.", "category": "bracelet"}
]

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"})

@app.route('/auth/signup', methods=['POST'])
def signup():
    return jsonify({"access_token": "test_token", "user_id": "test_user"})

@app.route('/auth/login', methods=['POST'])
def login():
    return jsonify({"access_token": "test_token", "user_id": "test_user"})

@app.route('/chat/sessions', methods=['POST'])
def create_session():
    return jsonify({"session_id": "test_session_123"})

@app.route('/chat/history/<session_id>', methods=['GET'])
def get_history(session_id):
    # Simulate slow response to increase chance of race condition
    time.sleep(0.5)
    return jsonify({"messages": chat_history})

@app.route('/chat/query', methods=['POST'])
def chat_query():
    data = request.get_json()
    query = data.get('query', '').lower()
    
    # Simulate processing time
    time.sleep(0.3)
    
    # Simulate different responses based on query
    if 'necklace' in query:
        response_text = "Absolutely! Switching over to necklaces for you. I found a beautiful Pearl Strand Necklace for $399.99. It's an elegant 18-inch strand of AAA-grade freshwater pearls with a lovely gold clasp."
        products = [p for p in current_products if p['category'] == 'necklace']
        
    elif 'watch' in query:
        response_text = "Perfect! I found some great watches for you. Here's a Men's Chronograph Watch for $699.99 with stainless steel construction and sapphire crystal."
        products = [p for p in current_products if p['category'] == 'watch']
        
    elif 'similar' in query:
        # This is where the sync issue might occur - text about necklaces but products are watches
        response_text = "Absolutely! Switching over to necklaces for you. I found a beautiful Pearl Strand Necklace for $399.99. It's an elegant 18-inch strand of AAA-grade freshwater pearls with a lovely gold clasp."
        products = [p for p in current_products if p['category'] == 'watch']  # Intentionally mismatched!
        
    else:
        response_text = "I found some beautiful jewelry pieces for you:"
        products = current_products[:3]
    
    # Add to chat history
    chat_history.append({
        "role": "user",
        "content": data.get('query', ''),
        "products": None
    })
    chat_history.append({
        "role": "assistant",
        "content": response_text,
        "products": products
    })
    
    return jsonify({
        "response": response_text,
        "products": products,
        "session_id": "test_session_123"
    })

if __name__ == '__main__':
    print("Starting test server on http://localhost:5000")
    print("This server simulates the race condition scenario")
    app.run(debug=True, port=5000)