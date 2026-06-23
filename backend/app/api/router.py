from fastapi import APIRouter

from app.api.health import router as health_router
from app.modules.categories.router import router as categories_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(categories_router)