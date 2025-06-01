from fastapi import HTTPException, status, Header
from typing import Optional
from ..config import settings


async def verify_auth_token(authorization: Optional[str] = Header(None)) -> str:
    """Verify the authorization token."""
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header is required"
        )
    
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization format. Use 'Bearer <token>'"
        )
    
    token = authorization.replace("Bearer ", "")
    if token != settings.auth_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization token"
        )
    
    return token 