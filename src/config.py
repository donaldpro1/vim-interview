from pydantic_settings import BaseSettings
from typing import Dict


class Settings(BaseSettings):
    app_name: str = "User Notifications Manager"
    app_version: str = "1.0.0"
    auth_token: str = "onlyvim2024"
    notification_service_url: str = "http://notification-service:5001"
    
    class Config:
        env_file = ".env"


settings = Settings() 