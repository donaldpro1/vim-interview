# Test Send Notification Endpoint
Write-Host "Testing Send Notification Endpoint..." -ForegroundColor Green

# Test 1: User with both email and SMS enabled (userId: 1)
Write-Host "`n1. Testing user with both email and SMS enabled (Iron Man):" -ForegroundColor Yellow
$response1 = curl -X POST -H "Authorization: Bearer onlyvim2024" -H "Content-Type: application/json" -d "{`"userId`": 1, `"message`": `"Hello Iron Man!`"}" http://localhost:8000/notifications/send
Write-Host $response1

# Test 2: User with only email enabled (userId: 2)
Write-Host "`n2. Testing user with only email enabled (Loki):" -ForegroundColor Yellow
$response2 = curl -X POST -H "Authorization: Bearer onlyvim2024" -H "Content-Type: application/json" -d "{`"userId`": 2, `"message`": `"Hello Loki!`"}" http://localhost:8000/notifications/send
Write-Host $response2

# Test 3: User with all notifications disabled (userId: 3)
Write-Host "`n3. Testing user with all notifications disabled (Hulk):" -ForegroundColor Yellow
$response3 = curl -X POST -H "Authorization: Bearer onlyvim2024" -H "Content-Type: application/json" -d "{`"userId`": 3, `"message`": `"Hello Hulk!`"}" http://localhost:8000/notifications/send
Write-Host $response3

# Test 4: Non-existent user
Write-Host "`n4. Testing non-existent user:" -ForegroundColor Yellow
$response4 = curl -X POST -H "Authorization: Bearer onlyvim2024" -H "Content-Type: application/json" -d "{`"userId`": 999, `"message`": `"Hello Nobody!`"}" http://localhost:8000/notifications/send
Write-Host $response4

# Test 5: No authorization
Write-Host "`n5. Testing without authorization:" -ForegroundColor Yellow
$response5 = curl -X POST -H "Content-Type: application/json" -d "{`"userId`": 1, `"message`": `"Unauthorized test`"}" http://localhost:8000/notifications/send
Write-Host $response5

Write-Host "`nTesting completed!" -ForegroundColor Green 