from pydantic import BaseModel, EmailStr
from typing import Dict, Optional


class NotificationPreferences(BaseModel):
    email: bool
    sms: bool


class UserPreference(BaseModel):
    userId: int
    email: EmailStr
    telephone: str
    preferences: NotificationPreferences


class CreateUserRequest(BaseModel):
    email: EmailStr
    telephone: str
    preferences: NotificationPreferences


class UpdateUserRequest(BaseModel):
    email: EmailStr
    telephone: Optional[str] = None
    preferences: NotificationPreferences


class NotificationRequest(BaseModel):
    userId: int
    message: str


class NotificationResponse(BaseModel):
    success: bool
    message: str
    userId: Optional[int] = None 