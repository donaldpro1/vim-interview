import requests
from typing import Dict, Any
from .models import UserPreference


class NotificationService:
    def __init__(self, base_url: str = "http://notification-service:5001"):
        self.base_url = base_url
    
    def send_email(self, email: str, message: str) -> Dict[str, Any]:
        """Send email notification via external service."""
        try:
            response = requests.post(
                f"{self.base_url}/send-email",
                json={"email": email, "message": message},
                timeout=10
            )
            return {"success": response.status_code == 200, "response": response.json()}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def send_sms(self, telephone: str, message: str) -> Dict[str, Any]:
        """Send SMS notification via external service."""
        try:
            response = requests.post(
                f"{self.base_url}/send-sms",
                json={"telephone": telephone, "message": message},
                timeout=10
            )
            return {"success": response.status_code == 200, "response": response.json()}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def send_notification(self, user: UserPreference, message: str) -> Dict[str, Any]:
        """Send notification based on user preferences."""
        results = {"email": None, "sms": None}
        
        if user.preferences.email:
            results["email"] = self.send_email(user.email, message)
        
        if user.preferences.sms:
            results["sms"] = self.send_sms(user.telephone, message)
        
        return results 