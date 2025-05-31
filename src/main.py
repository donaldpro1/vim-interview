from fastapi import FastAPI, HTTPException, status
from typing import List, Dict
from .models import UserPreference, NotificationRequest, NotificationResponse, NotificationPreferences
from .notification_service import NotificationService

app = FastAPI(title="User Notifications Manager", version="1.0.0")

# Simple in-memory storage for user preferences
user_preferences: Dict[int, UserPreference] = {
    1: UserPreference(
        userId=1,
        email="ironman@avengers.com",
        telephone="+123456789",
        preferences=NotificationPreferences(email=True, sms=True)
    ),
    2: UserPreference(
        userId=2,
        email="loki@avengers.com",
        telephone="+123456788",
        preferences=NotificationPreferences(email=True, sms=False)
    ),
    3: UserPreference(
        userId=3,
        email="hulk@avengers.com",
        telephone="+123456787",
        preferences=NotificationPreferences(email=False, sms=False)
    ),
    4: UserPreference(
        userId=4,
        email="blackwidow@avengers.com",
        telephone="+123456786",
        preferences=NotificationPreferences(email=True, sms=True)
    )
}

notification_service = NotificationService()


@app.get("/")
def read_root():
    """Health check endpoint."""
    return {"message": "User Notifications Manager is running"}


@app.get("/users", response_model=List[UserPreference])
def get_all_users():
    """Get all user preferences."""
    return list(user_preferences.values())


@app.get("/users/{user_id}", response_model=UserPreference)
def get_user_preferences(user_id: int):
    """Get preferences for a specific user."""
    if user_id not in user_preferences:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    return user_preferences[user_id]


@app.post("/users", response_model=UserPreference, status_code=status.HTTP_201_CREATED)
def create_user_preferences(user: UserPreference):
    """Create new user preferences."""
    if user.userId in user_preferences:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with ID {user.userId} already exists"
        )
    user_preferences[user.userId] = user
    return user


@app.put("/users/{user_id}", response_model=UserPreference)
def update_user_preferences(user_id: int, user: UserPreference):
    """Update existing user preferences."""
    if user_id not in user_preferences:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    user.userId = user_id  # Ensure consistency
    user_preferences[user_id] = user
    return user


@app.delete("/users/{user_id}")
def delete_user_preferences(user_id: int):
    """Delete user preferences."""
    if user_id not in user_preferences:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    del user_preferences[user_id]
    return {"message": f"User {user_id} preferences deleted successfully"}


@app.post("/notifications/send", response_model=NotificationResponse)
def send_notification(request: NotificationRequest):
    """Send notification to a user based on their preferences."""
    if request.userId not in user_preferences:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {request.userId} not found"
        )
    
    user = user_preferences[request.userId]
    
    # Check if user has any notification preferences enabled
    if not user.preferences.email and not user.preferences.sms:
        return NotificationResponse(
            success=False,
            message="User has disabled all notification preferences",
            userId=request.userId
        )
    
    # Send notification via external service
    results = notification_service.send_notification(user, request.message)
    
    # Check if any notification was successful
    success = False
    if results.get("email") and results["email"].get("success"):
        success = True
    if results.get("sms") and results["sms"].get("success"):
        success = True
    
    return NotificationResponse(
        success=success,
        message="Notification sent successfully" if success else "Failed to send notification",
        userId=request.userId
    ) 