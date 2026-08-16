"""Re-export Base for convenient import by Alembic and models."""

from app.db.session import Base

__all__ = ["Base"]
