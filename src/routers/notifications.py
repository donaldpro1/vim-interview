from fastapi import APIRouter, Depends
from ..data.models import NotificationRequest, NotificationResponse
from ..services.notification_service import notification_service
from .auth import verify_auth_token

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.post("/send", response_model=NotificationResponse)
async def send_notification(request: NotificationRequest, token: str = Depends(verify_auth_token)):
    """Send notification to a user based on their preferences."""
    return await notification_service.send_notification(request) 