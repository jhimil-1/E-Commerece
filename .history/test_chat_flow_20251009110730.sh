#!/bin/bash

# Test the complete flow: login -> create session -> chat query

echo "=== Step 1: Login ==="
LOGIN_RESPONSE=$(curl -s -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser1",
    "password": "testpass123"
  }')

echo "Login response: $LOGIN_RESPONSE"

# Extract token using jq (if available) or manually
TOKEN=$(echo $LOGIN_RESPONSE | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)
echo "Extracted token: $TOKEN"

echo ""
echo "=== Step 2: Create Session ==="
SESSION_RESPONSE=$(curl -s -X POST "http://localhost:8000/chat/sessions" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json")

echo "Session response: $SESSION_RESPONSE"

# Extract session ID
SESSION_ID=$(echo $SESSION_RESPONSE | grep -o '"session_id":"[^"]*' | cut -d'"' -f4)
echo "Extracted session ID: $SESSION_ID"

echo ""
echo "=== Step 3: Chat Query ==="
QUERY_RESPONSE=$(curl -s -X POST "http://localhost:8000/chat/query" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"query\": \"laptop\",
    \"session_id\": \"$SESSION_ID\"
  }")

echo "Chat query response: $QUERY_RESPONSE"

# Count products in response
PRODUCT_COUNT=$(echo $QUERY_RESPONSE | grep -o '"name":' | wc -l)
echo "Number of products found: $PRODUCT_COUNT"