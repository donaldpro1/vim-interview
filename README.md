# User Notifications Manager

A FastAPI-based backend service for managing user notification preferences and sending notifications via email and SMS channels.

## Overview

This service manages user notification preferences and sends notifications through an external Notification Service. It supports email and SMS channels with flexible preference management.

## Features

- **User Management**: Create and update user notification preferences
- **Notification Sending**: Send notifications based on user preferences
- **Multi-Channel Support**: Email and SMS notifications
- **In-Memory Storage**: Fast access for hundreds of thousands of users
- **Docker Support**: Containerized deployment with Docker Compose
- **RESTful API**: Clean HTTP endpoints with proper authentication

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.8+ (for local development)

### Run with Docker Compose

1. Start all services:
```bash
docker-compose up --build
```

2. Access the services:
   - **User Notifications Manager**: http://localhost:8080
   - **Notification Service**: http://localhost:5001

3. Stop services:
```bash
docker-compose down
```

### Local Development

1. Create virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the service:
```bash
uvicorn src.main:app --host 0.0.0.0 --port 8080 --reload
```

## API Endpoints

All endpoints require authentication header:
```
Authorization: Bearer onlyvim2024
```

### 1. Send Notification

**POST** `/notifications`

Send a notification to a user based on their preferences.

**Request Body:**
```json
{
  "userId": 1,
  "message": "Your notification message here"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Notifications sent successfully",
  "sent_channels": ["email", "sms"]
}
```

### 2. Create User

**POST** `/users`

Create a new user with notification preferences.

**Request Body:**
```json
{
  "email": "user@example.com",
  "telephone": "+1234567890",
  "preferences": {
    "email": true,
    "sms": true
  }
}
```

**Response:**
```json
{
  "userId": 5,
  "email": "user@example.com",
  "telephone": "+1234567890",
  "preferences": {
    "email": true,
    "sms": true
  }
}
```

### 3. Update User Preferences

**PUT** `/users/{user_id}/preferences`

Update notification preferences for an existing user.

**Request Body:**
```json
{
  "preferences": {
    "email": false,
    "sms": true
  }
}
```

### 4. Get User

**GET** `/users/{user_id}`

Retrieve user information and preferences.

## Usage Examples

### Send a notification:
```bash
curl -X POST http://localhost:8080/notifications \
  -H "Authorization: Bearer onlyvim2024" \
  -H "Content-Type: application/json" \
  -d '{
    "userId": 1,
    "message": "Hello, this is a test notification!"
  }'
```

### Create a new user:
```bash
curl -X POST http://localhost:8080/users \
  -H "Authorization: Bearer onlyvim2024" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newuser@example.com",
    "telephone": "+1234567890",
    "preferences": {
      "email": true,
      "sms": false
    }
  }'
```

### Update user preferences:
```bash
curl -X PUT http://localhost:8080/users/1/preferences \
  -H "Authorization: Bearer onlyvim2024" \
  -H "Content-Type: application/json" \
  -d '{
    "preferences": {
      "email": false,
      "sms": true
    }
  }'
```

## Project Structure

```
/
├── src/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application and endpoints
│   ├── models.py               # Pydantic data models
│   └── notification_service.py # External notification service client
├── docker-compose.yml          # Multi-service orchestration
├── Dockerfile                  # Container configuration
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Default Users

The service comes with pre-loaded test users:

| User ID | Email | Phone | Email Pref | SMS Pref |
|---------|-------|-------|------------|----------|
| 1 | ironman@avengers.com | +123456789 | ✓ | ✓ |
| 2 | loki@avengers.com | +123456788 | ✓ | ✗ |
| 3 | hulk@avengers.com | +123456787 | ✗ | ✗ |
| 4 | blackwidow@avengers.com | +123456786 | ✓ | ✓ |

## Error Handling

The service handles various error scenarios:

- **404**: User not found
- **400**: Invalid request data
- **401**: Missing or invalid authentication
- **500**: External service errors (with retry logic)

## Technology Stack

- **FastAPI**: Modern Python web framework
- **Pydantic**: Data validation and serialization
- **Uvicorn**: ASGI server
- **Docker**: Containerization
- **Requests**: HTTP client for external API calls

## Testing

Test the service functionality:

1. **Health Check**:
```bash
curl http://localhost:8080/health
```

2. **Send Test Notification**:
```bash
curl -X POST http://localhost:8080/notifications \
  -H "Authorization: Bearer onlyvim2024" \
  -H "Content-Type: application/json" \
  -d '{"userId": 1, "message": "Test message"}'
```

## Development Notes

- Data is stored in memory for fast access
- Service supports hundreds of thousands of users
- Designed for easy extension with additional notification channels
- Includes proper error handling and logging
- Authentication required for all endpoints

## License

This project is part of a technical assessment for VIM. 