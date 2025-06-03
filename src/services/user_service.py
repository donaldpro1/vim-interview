from fastapi import HTTPException, status
from typing import List
from ..data.models import UserPreference, CreateUserRequest, UpdateUserRequest
from ..data.database import user_db


class UserService:
    """Service class for user-related operations."""
    
    def get_all_users(self) -> List[UserPreference]:
        """Get all user preferences."""
        return user_db.get_all_users()
    
    def get_user_by_id(self, user_id: int) -> UserPreference:
        """Get user preferences by ID."""
        user = user_db.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found"
            )
        return user
    
    def create_user(self, user_request: CreateUserRequest) -> UserPreference:
        """Create new user preferences."""
        # Check if user with this email already exists
        if user_db.user_exists_by_email(user_request.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User with email {user_request.email} already exists"
            )
        
        # Create new user with auto-generated ID
        user_id = user_db.get_next_user_id()
        user = UserPreference(
            userId=user_id,
            email=user_request.email,
            telephone=user_request.telephone,
            preferences=user_request.preferences
        )
        
        return user_db.create_user(user)
    
    def update_user_by_email(self, user_request: UpdateUserRequest) -> UserPreference:
        """Update existing user preferences by email."""
        existing_user = user_db.get_user_by_email(user_request.email)
        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with email {user_request.email} not found"
            )
        
        # Update preferences
        existing_user.preferences = user_request.preferences
        if hasattr(user_request, 'telephone') and user_request.telephone:
            existing_user.telephone = user_request.telephone
        
        return user_db.update_user(existing_user.userId, existing_user)
    
    def update_user_by_id(self, user_id: int, user: UserPreference) -> UserPreference:
        """Update existing user preferences by ID."""
        if not user_db.user_exists_by_id(user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found"
            )
        
        return user_db.update_user(user_id, user)
    
    def delete_user(self, user_id: int) -> dict:
        """Delete user preferences."""
        if not user_db.user_exists_by_id(user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found"
            )
        
        user_db.delete_user(user_id)
        return {"message": f"User {user_id} preferences deleted successfully"}


# Global service instance
user_service = UserService() 