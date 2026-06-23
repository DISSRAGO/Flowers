from fastapi import APIRouter

from app.core.config import settings

router = APIRouter(tags=["health"])


@router.get("/health")
async def healthcheck():
    return {
        "status": "ok",
        "service": "flowers-backend",
        "environment": settings.app_env,
        "database_configured": bool(settings.database_url),
    }