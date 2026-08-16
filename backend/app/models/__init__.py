"""Models package — import all models so Alembic and Base.metadata can see them."""

from app.models.user import User, UserRole
from app.models.property import Property, PropertyType, PropertyStatus
from app.models.chat import Conversation, Message, MessageRole
from app.models.favorite import Favorite
from app.models.analytics import SearchAnalytics

__all__ = [
    "User",
    "UserRole",
    "Property",
    "PropertyType",
    "PropertyStatus",
    "Conversation",
    "Message",
    "MessageRole",
    "Favorite",
    "SearchAnalytics",
]
