"""FastAPI dependency injection utilities."""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services.user_service import UserService
from app.services.property_service import PropertyService
from app.services.chat_service import ChatService
from app.services.vector_service import VectorService
from app.utils.auth import get_current_user


async def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(db)


async def get_property_service(db: AsyncSession = Depends(get_db)) -> PropertyService:
    return PropertyService(db)


async def get_chat_service(db: AsyncSession = Depends(get_db)) -> ChatService:
    return ChatService(db)


def get_vector_service() -> VectorService:
    return VectorService()
