"""Schemas package."""

from app.schemas.user import UserRegister, UserLogin, UserResponse, TokenResponse, TokenRefreshRequest
from app.schemas.property import (
    PropertyCreate, PropertyUpdate, PropertySearch,
    PropertyResponse, PropertyListResponse,
)
from app.schemas.chat import (
    ChatMessageRequest, MessageResponse,
    ConversationResponse, ConversationDetailResponse, ChatResponse,
)
from app.schemas.analytics import SearchAnalyticsResponse, DashboardAnalytics

__all__ = [
    "UserRegister", "UserLogin", "UserResponse", "TokenResponse", "TokenRefreshRequest",
    "PropertyCreate", "PropertyUpdate", "PropertySearch",
    "PropertyResponse", "PropertyListResponse",
    "ChatMessageRequest", "MessageResponse",
    "ConversationResponse", "ConversationDetailResponse", "ChatResponse",
    "SearchAnalyticsResponse", "DashboardAnalytics",
]
