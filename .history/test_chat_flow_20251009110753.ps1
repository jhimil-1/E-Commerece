# Test the complete flow: login -> create session -> chat query

Write-Host "=== Step 1: Login ==="
$loginResponse = Invoke-RestMethod -Uri "http://localhost:8000/auth/login" -Method Post -ContentType "application/json" -Body '{
    "username": "testuser1",
    "password": "testpass123"
}'

Write-Host "Login response: $($loginResponse | ConvertTo-Json -Depth 10)"
$token = $loginResponse.access_token
Write-Host "Extracted token: $token"

Write-Host ""
Write-Host "=== Step 2: Create Session ==="
$headers = @{
    "Authorization" = "Bearer $token"
    "Content-Type" = "application/json"
}

$sessionResponse = Invoke-RestMethod -Uri "http://localhost:8000/chat/sessions" -Method Post -Headers $headers
Write-Host "Session response: $($sessionResponse | ConvertTo-Json -Depth 10)"
$sessionId = $sessionResponse.session_id
Write-Host "Extracted session ID: $sessionId"

Write-Host ""
Write-Host "=== Step 3: Chat Query ==="
$queryBody = @{
    query = "laptop"
    session_id = $sessionId
} | ConvertTo-Json

$queryResponse = Invoke-RestMethod -Uri "http://localhost:8000/chat/query" -Method Post -Headers $headers -Body $queryBody
Write-Host "Chat query response: $($queryResponse | ConvertTo-Json -Depth 10)"

$productCount = ($queryResponse.products | Measure-Object).Count
Write-Host "Number of products found: $productCount"