"""Pydantic schemas for Property requests and responses."""

import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from app.models.property import PropertyType, PropertyStatus


# ── Request Schemas ─────────────────────────────────────

class PropertyCreate(BaseModel):
    title: str = Field(..., max_length=500)
    description: str | None = None
    price: float = Field(..., gt=0)
    property_type: PropertyType
    bedrooms: int | None = Field(None, ge=0)
    bathrooms: int | None = Field(None, ge=0)
    area_sqft: float | None = Field(None, gt=0)
    address: str = Field(..., max_length=500)
    city: str = Field(..., max_length=255)
    state: str = Field(..., max_length=100)
    zip_code: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    features: dict = Field(default_factory=dict)
    images: list[str] = Field(default_factory=list)
    year_built: int | None = None
    lot_size_sqft: float | None = None
    parking_spaces: int | None = None
    hoa_monthly: float | None = None


class PropertyUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    price: float | None = Field(None, gt=0)
    property_type: PropertyType | None = None
    bedrooms: int | None = None
    bathrooms: int | None = None
    area_sqft: float | None = None
    address: str | None = None
    city: str | None = None
    state: str | None = None
    zip_code: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    features: dict | None = None
    images: list[str] | None = None
    status: PropertyStatus | None = None
    year_built: int | None = None
    lot_size_sqft: float | None = None
    parking_spaces: int | None = None
    hoa_monthly: float | None = None


class PropertySearch(BaseModel):
    """Query parameters for searching properties."""
    city: str | None = None
    state: str | None = None
    zip_code: str | None = None
    property_type: PropertyType | None = None
    min_price: float | None = None
    max_price: float | None = None
    min_bedrooms: int | None = None
    max_bedrooms: int | None = None
    min_bathrooms: int | None = None
    min_area_sqft: float | None = None
    max_area_sqft: float | None = None
    status: PropertyStatus = PropertyStatus.ACTIVE
    sort_by: str = "listed_at"
    sort_order: str = "desc"
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)


# ── Response Schemas ────────────────────────────────────

class PropertyResponse(BaseModel):
    id: uuid.UUID
    title: str
    description: str | None
    price: float
    property_type: PropertyType
    bedrooms: int | None
    bathrooms: int | None
    area_sqft: float | None
    address: str
    city: str
    state: str
    zip_code: str | None
    latitude: float | None
    longitude: float | None
    features: dict
    images: list
    status: PropertyStatus
    year_built: int | None
    lot_size_sqft: float | None
    parking_spaces: int | None
    hoa_monthly: float | None
    listed_at: datetime
    updated_at: datetime
    price_per_sqft: float | None = None

    model_config = {"from_attributes": True}


class PropertyListResponse(BaseModel):
    properties: list[PropertyResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
