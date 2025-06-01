# Test script for User Notifications Manager API
$baseUrl = "http://localhost:8080"
$headers = @{
    'Authorization' = 'Bearer onlyvim2024'
    'Content-Type' = 'application/json'
}

Write-Host "Testing User Notifications Manager API..." -ForegroundColor Green

# Test 1: Health check
Write-Host "`n1. Testing health check..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/" -Method GET
    Write-Host "✓ Health check passed: $($response.message)" -ForegroundColor Green
} catch {
    Write-Host "✗ Health check failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 2: Get all users
Write-Host "`n2. Testing get all users..." -ForegroundColor Yellow
try {
    $users = Invoke-RestMethod -Uri "$baseUrl/users" -Method GET -Headers $headers
    Write-Host "✓ Retrieved $($users.Count) users" -ForegroundColor Green
    $users | ForEach-Object { Write-Host "  - User $($_.userId): $($_.email)" }
} catch {
    Write-Host "✗ Get users failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 3: Send notification
Write-Host "`n3. Testing send notification..." -ForegroundColor Yellow
try {
    $notificationData = @{
        userId = 1
        message = "Test notification from PowerShell script"
    } | ConvertTo-Json
    
    $response = Invoke-RestMethod -Uri "$baseUrl/notifications/send" -Method POST -Headers $headers -Body $notificationData
    Write-Host "✓ Notification sent successfully: $($response.message)" -ForegroundColor Green
} catch {
    Write-Host "✗ Send notification failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 4: Create new user
Write-Host "`n4. Testing create new user..." -ForegroundColor Yellow
try {
    $newUserData = @{
        email = "testuser@example.com"
        telephone = "+1234567890"
        preferences = @{
            email = $true
            sms = $false
        }
    } | ConvertTo-Json
    
    $response = Invoke-RestMethod -Uri "$baseUrl/users" -Method POST -Headers $headers -Body $newUserData
    Write-Host "✓ User created successfully: User $($response.userId) - $($response.email)" -ForegroundColor Green
    $newUserId = $response.userId
} catch {
    Write-Host "✗ Create user failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 5: Update user preferences by email
Write-Host "`n5. Testing update user preferences..." -ForegroundColor Yellow
try {
    $updateData = @{
        email = "testuser@example.com"
        preferences = @{
            email = $false
            sms = $true
        }
    } | ConvertTo-Json
    
    $response = Invoke-RestMethod -Uri "$baseUrl/users" -Method PUT -Headers $headers -Body $updateData
    Write-Host "✓ User preferences updated: Email=$($response.preferences.email), SMS=$($response.preferences.sms)" -ForegroundColor Green
} catch {
    Write-Host "✗ Update user failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "All tests completed!" -ForegroundColor Green 