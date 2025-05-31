from pydantic import BaseModel
from typing import Dict, Optional


class NotificationPreferences(BaseModel):
    email: bool
    sms: bool


class UserPreference(BaseModel):
    userId: int
    email: str
    telephone: str
    preferences: NotificationPreferences


class NotificationRequest(BaseModel):
    userId: int
    message: str


class NotificationResponse(BaseModel):
    success: bool
    message: str
    userId: Optional[int] = None 