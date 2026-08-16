"""Search analytics model — tracks user search patterns."""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Integer, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class SearchAnalytics(Base):
    __tablename__ = "search_analytics"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    query_text: Mapped[str | None] = mapped_column(nullable=True)
    query_params: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    query_type: Mapped[str | None] = mapped_column(nullable=True)
    results_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    response_time_ms: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    searched_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True,
    )

    # Relationships
    user = relationship("User", back_populates="search_analytics")

    def __repr__(self) -> str:
        return f"<SearchAnalytics user={self.user_id} at={self.searched_at}>"
