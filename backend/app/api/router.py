"""API Router — aggregates all v1 route modules."""

from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.properties import router as properties_router
from app.api.v1.chat import router as chat_router
from app.api.v1.favorites import router as favorites_router
from app.api.v1.analytics import router as analytics_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth_router)
api_router.include_router(properties_router)
api_router.include_router(chat_router)
api_router.include_router(favorites_router)
api_router.include_router(analytics_router)
