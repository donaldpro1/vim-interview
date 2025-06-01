from fastapi import FastAPI
from .config import settings
from .routers import users_router, notifications_router

app = FastAPI(title=settings.app_name, version=settings.app_version)

# Include routers
app.include_router(users_router)
app.include_router(notifications_router)


@app.get("/")
async def read_root():
    """Health check endpoint."""
    return {"message": f"{settings.app_name} is running"} 