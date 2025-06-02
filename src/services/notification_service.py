import httpx
from typing import Dict, Any, Optional
from fastapi import HTTPException, status
from ..data.models import UserPreference, NotificationRequest, NotificationResponse
from ..data.database import user_db
from ..config import settings


class NotificationService:
    """Notification service that handles user lookup and external API communication."""
    
    def __init__(self, base_url: str = None):
        self.base_url = base_url or settings.notification_service_url
        self.timeout = 10.0
    
    async def _make_api_request(self, endpoint: str, payload: Dict[str, str]) -> Dict[str, Any]:
        """Make an async HTTP request to the external notification service."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/{endpoint}",
                    json=payload,
                    headers={"Content-Type": "application/json"}
                )
                
                # Handle successful response
                if response.status_code == 200:
                    response_data = await self._parse_response(response)
                    return {"success": True, "data": response_data}
                
                # Handle error responses
                error_message = await self._extract_error_message(response)
                return {"success": False, "error": error_message}
                
        except httpx.TimeoutException:
            return {"success": False, "error": "Request timeout - external service not responding"}
        except httpx.ConnectError:
            return {"success": False, "error": "Connection failed - external service unavailable"}
        except Exception as e:
            return {"success": False, "error": f"Unexpected error: {str(e)}"}
    
    async def _parse_response(self, response: httpx.Response) -> Dict[str, Any]:
        """Parse the response from external service."""
        try:
            return response.json()
        except Exception:
            return {"message": "Response received but could not parse JSON"}
    
    async def _extract_error_message(self, response: httpx.Response) -> str:
        """Extract error message from failed response."""
        try:
            if response.headers.get("content-type", "").startswith("application/json"):
                error_data = response.json()
                return error_data.get("error", f"HTTP {response.status_code}")
            else:
                return f"HTTP {response.status_code} - {response.reason_phrase}"
        except Exception:
            return f"HTTP {response.status_code} - Unknown error"
    
    async def _send_email(self, email: str, message: str) -> Dict[str, Any]:
        """Send email notification via external service."""
        payload = {"email": email, "message": message}
        return await self._make_api_request("send-email", payload)
    
    async def _send_sms(self, telephone: str, message: str) -> Dict[str, Any]:
        """Send SMS notification via external service."""
        payload = {"telephone": telephone, "message": message}
        return await self._make_api_request("send-sms", payload)
    
    async def _send_user_notification(self, user: UserPreference, message: str) -> Dict[str, Any]:
        """Send notification to a user based on their preferences."""
        results = {"email": None, "sms": None}
        
        # Send email if enabled
        if user.preferences.email:
            results["email"] = await self._send_email(user.email, message)
        
        # Send SMS if enabled
        if user.preferences.sms:
            results["sms"] = await self._send_sms(user.telephone, message)
        
        return results
    
    async def send_notification(self, request: NotificationRequest) -> NotificationResponse:
        """Send notification to a user based on their preferences."""
        # Get user from database
        user = user_db.get_user_by_id(request.userId)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {request.userId} not found"
            )
        
        # Check if user has any notification preferences enabled
        if not user.preferences.email and not user.preferences.sms:
            return NotificationResponse(
                success=False,
                message="User has disabled all notification preferences",
                userId=request.userId
            )
        
        # Send notification via external service
        results = await self._send_user_notification(user, request.message)
        
        # Process results and create response
        return self._create_response(results, request.userId)
    
    def _create_response(self, results: Dict[str, Any], user_id: int) -> NotificationResponse:
        """Create notification response based on results."""
        # Check if any notification was successful
        success = any(
            result.get("success", False) 
            for result in results.values() 
            if result is not None
        )
        
        # Build status message
        statuses = []
        for channel, result in results.items():
            if result is None:
                continue
            status = "succeeded" if result.get("success", False) else "failed"
            statuses.append(f"{channel.upper()} {status}")
        
        message = " and ".join(statuses) if statuses else "No notifications sent"
        
        return NotificationResponse(
            success=success,
            message=message,
            userId=user_id
        )


# Global service instance
notification_service = NotificationService() 