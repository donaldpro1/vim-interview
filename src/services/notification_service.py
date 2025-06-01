import asyncio
import httpx
from typing import Dict, Any, Optional
from fastapi import HTTPException, status
from ..data.models import UserPreference, NotificationRequest, NotificationResponse
from ..database import user_db
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
        """Send notification to a user based on their preferences concurrently."""
        results = {"email": None, "sms": None}
        
        # Prepare tasks for concurrent execution
        tasks = []
        if user.preferences.email:
            tasks.append(("email", self._send_email(user.email, message)))
        
        if user.preferences.sms:
            tasks.append(("sms", self._send_sms(user.telephone, message)))
        
        # Execute all tasks concurrently if any exist
        if not tasks:
            return results
        
        try:
            # Use asyncio.gather for concurrent execution
            task_results = await asyncio.gather(
                *[task[1] for task in tasks], 
                return_exceptions=True
            )
            
            # Map results back to their channels
            for i, (channel, _) in enumerate(tasks):
                result = task_results[i]
                if isinstance(result, Exception):
                    results[channel] = {
                        "success": False, 
                        "error": f"Task failed: {str(result)}"
                    }
                else:
                    results[channel] = result
                    
        except Exception as e:
            # Handle unexpected errors in concurrent execution
            for channel, _ in tasks:
                results[channel] = {
                    "success": False, 
                    "error": f"Concurrent execution failed: {str(e)}"
                }
        
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
        
        # Send notification via external service (async and concurrent)
        results = await self._send_user_notification(user, request.message)
        
        # Process results and create response
        return self._create_response(results, request.userId)
    
    def _create_response(self, results: Dict[str, Any], user_id: int) -> NotificationResponse:
        """Create notification response based on results."""
        success = False
        success_messages = []
        error_messages = []
        
        # Process email results
        email_result = results.get("email")
        if email_result:
            if email_result.get("success"):
                success = True
                success_messages.append("Email sent successfully")
            else:
                error_messages.append(f"Email failed: {email_result.get('error', 'Unknown error')}")
        
        # Process SMS results
        sms_result = results.get("sms")
        if sms_result:
            if sms_result.get("success"):
                success = True
                success_messages.append("SMS sent successfully")
            else:
                error_messages.append(f"SMS failed: {sms_result.get('error', 'Unknown error')}")
        
        # Create response message
        if success:
            if error_messages:
                message = f"{'; '.join(success_messages)}. {'; '.join(error_messages)}"
            else:
                message = "; ".join(success_messages)
        else:
            message = f"Failed to send notification: {'; '.join(error_messages)}"
        
        return NotificationResponse(
            success=success,
            message=message,
            userId=user_id
        )


# Global service instance
notification_service = NotificationService() 