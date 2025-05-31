# User Notifications Manager

A simple FastAPI service for managing user notification preferences and sending notifications.

## Features

- Manage user notification preferences (email/SMS)
- Send notifications based on user preferences
- Integration with external notification service
- RESTful API with proper HTTP status codes
- Docker containerization

## Quick Start

### Using Docker Compose (Recommended)

1. Start the services:
```bash
docker-compose up --build
```

2. The API will be available at: `http://localhost:8080`
3. API documentation: `http://localhost:8080/docs`

### Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
uvicorn src.main:app --reload --port 8080
```

## API Endpoints

### User Preferences Management
- `GET /users` - Get all users
- `GET /users/{user_id}` - Get specific user preferences
- `POST /users` - Create new user preferences
- `PUT /users/{user_id}` - Update user preferences
- `DELETE /users/{user_id}` - Delete user preferences

### Notifications
- `POST /notifications/send` - Send notification to user

## Testing the Service

### 1. Check if service is running:
```bash
curl http://localhost:8080/
```

### 2. Get all users:
```bash
curl http://localhost:8080/users
```

### 3. Send a notification:
```bash
curl -X POST http://localhost:8080/notifications/send \
  -H "Content-Type: application/json" \
  -d '{"userId": 1, "message": "Hello Iron Man!"}'
```

### 4. Update user preferences:
```bash
curl -X PUT http://localhost:8080/users/1 \
  -H "Content-Type: application/json" \
  -d '{
    "userId": 1,
    "email": "ironman@avengers.com",
    "telephone": "+123456789",
    "preferences": {"email": true, "sms": false}
  }'
```

## Default Users

The service comes with 4 pre-configured users:
1. Iron Man (email + SMS enabled)
2. Loki (email only)
3. Hulk (no notifications)
4. Black Widow (email + SMS enabled)

## Architecture

- **FastAPI**: Web framework with automatic API documentation
- **Pydantic**: Data validation and serialization
- **In-memory storage**: Simple storage for user preferences
- **External notification service**: Integration via HTTP requests 