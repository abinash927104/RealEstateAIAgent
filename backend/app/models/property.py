"""Property model — real estate listings with full attributes."""

import uuid
from datetime import datetime, timezone

from sqlalchemy import String, Text, Numeric, Integer, Float, DateTime, ForeignKey, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.db.session import Base


class PropertyType(str, enum.Enum):
    HOUSE = "house"
    APARTMENT = "apartment"
    CONDO = "condo"
    TOWNHOUSE = "townhouse"
    LAND = "land"
    COMMERCIAL = "commercial"


class PropertyStatus(str, enum.Enum):
    ACTIVE = "active"
    PENDING = "pending"
    SOLD = "sold"
    OFF_MARKET = "off_market"


class Property(Base):
    __tablename__ = "properties"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    price: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    property_type: Mapped[PropertyType] = mapped_column(
        SAEnum(PropertyType, name="property_type"),
        nullable=False,
        index=True,
    )
    bedrooms: Mapped[int] = mapped_column(Integer, nullable=True)
    bathrooms: Mapped[int] = mapped_column(Integer, nullable=True)
    area_sqft: Mapped[float] = mapped_column(Float, nullable=True)

    # Location
    address: Mapped[str] = mapped_column(String(500), nullable=False)
    city: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    state: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    zip_code: Mapped[str] = mapped_column(String(20), nullable=True, index=True)
    latitude: Mapped[float] = mapped_column(Float, nullable=True)
    longitude: Mapped[float] = mapped_column(Float, nullable=True)

    # Metadata
    features: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    images: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    status: Mapped[PropertyStatus] = mapped_column(
        SAEnum(PropertyStatus, name="property_status"),
        default=PropertyStatus.ACTIVE,
        nullable=False,
        index=True,
    )
    year_built: Mapped[int] = mapped_column(Integer, nullable=True)
    lot_size_sqft: Mapped[float] = mapped_column(Float, nullable=True)
    parking_spaces: Mapped[int] = mapped_column(Integer, nullable=True)
    hoa_monthly: Mapped[float] = mapped_column(Numeric(10, 2), nullable=True)

    # Foreign keys
    owner_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=True
    )

    # Timestamps
    listed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    owner = relationship("User", back_populates="properties")
    favorites = relationship("Favorite", back_populates="property", lazy="selectin")

    def __repr__(self) -> str:
        return f"<Property {self.title} | ${self.price}>"

    @property
    def price_per_sqft(self) -> float | None:
        if self.area_sqft and self.area_sqft > 0:
            return float(self.price) / self.area_sqft
        return None
