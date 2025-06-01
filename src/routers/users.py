from fastapi import APIRouter, Depends, status
from typing import List
from ..data.models import UserPreference, CreateUserRequest, UpdateUserRequest
from ..services.user_service import user_service
from .auth import verify_auth_token

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=List[UserPreference])
async def get_all_users(token: str = Depends(verify_auth_token)):
    """Get all user preferences."""
    return user_service.get_all_users()


@router.get("/{user_id}", response_model=UserPreference)
async def get_user_preferences(user_id: int, token: str = Depends(verify_auth_token)):
    """Get preferences for a specific user."""
    return user_service.get_user_by_id(user_id)


@router.post("", response_model=UserPreference, status_code=status.HTTP_201_CREATED)
async def create_user_preferences(user_request: CreateUserRequest, token: str = Depends(verify_auth_token)):
    """Create new user preferences."""
    return user_service.create_user(user_request)


@router.put("", response_model=UserPreference)
async def update_user_preferences_by_email(user_request: UpdateUserRequest, token: str = Depends(verify_auth_token)):
    """Update existing user preferences by email."""
    return user_service.update_user_by_email(user_request)


@router.put("/{user_id}", response_model=UserPreference)
async def update_user_preferences(user_id: int, user: UserPreference, token: str = Depends(verify_auth_token)):
    """Update existing user preferences by ID."""
    return user_service.update_user_by_id(user_id, user)


@router.delete("/{user_id}")
async def delete_user_preferences(user_id: int, token: str = Depends(verify_auth_token)):
    """Delete user preferences."""
    return user_service.delete_user(user_id) 