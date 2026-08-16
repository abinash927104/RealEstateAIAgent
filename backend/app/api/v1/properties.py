"""Properties API routes — CRUD and search."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.property import PropertyType, PropertyStatus
from app.schemas.property import (
    PropertyCreate, PropertyUpdate, PropertySearch,
    PropertyResponse, PropertyListResponse,
)
from app.services.property_service import PropertyService
from app.services.vector_service import VectorService
from app.utils.auth import get_current_user

router = APIRouter(prefix="/properties", tags=["Properties"])


@router.get("", response_model=PropertyListResponse)
async def list_properties(
    city: str | None = None,
    state: str | None = None,
    zip_code: str | None = None,
    property_type: PropertyType | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    min_bedrooms: int | None = None,
    max_bedrooms: int | None = None,
    min_bathrooms: int | None = None,
    min_area_sqft: float | None = None,
    max_area_sqft: float | None = None,
    status: PropertyStatus = PropertyStatus.ACTIVE,
    sort_by: str = "listed_at",
    sort_order: str = "desc",
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """Search and list properties with filters and pagination."""
    service = PropertyService(db)
    params = PropertySearch(
        city=city, state=state, zip_code=zip_code,
        property_type=property_type,
        min_price=min_price, max_price=max_price,
        min_bedrooms=min_bedrooms, max_bedrooms=max_bedrooms,
        min_bathrooms=min_bathrooms,
        min_area_sqft=min_area_sqft, max_area_sqft=max_area_sqft,
        status=status,
        sort_by=sort_by, sort_order=sort_order,
        page=page, page_size=page_size,
    )
    result = await service.search(params)
    return PropertyListResponse(
        properties=[PropertyResponse.model_validate(p) for p in result["properties"]],
        total=result["total"],
        page=result["page"],
        page_size=result["page_size"],
        total_pages=result["total_pages"],
    )


@router.get("/{property_id}", response_model=PropertyResponse)
async def get_property(property_id: UUID, db: AsyncSession = Depends(get_db)):
    """Get a single property by ID."""
    service = PropertyService(db)
    prop = await service.get_by_id(property_id)
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    return PropertyResponse.model_validate(prop)


@router.post("", response_model=PropertyResponse, status_code=status.HTTP_201_CREATED)
async def create_property(
    data: PropertyCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Create a new property listing."""
    service = PropertyService(db)
    prop = await service.create(data, owner_id=current_user.id)

    # Also index in vector store
    try:
        vector_service = VectorService()
        await vector_service.add_property(str(prop.id), data.model_dump())
    except Exception:
        pass  # Don't fail the create if vector indexing fails

    return PropertyResponse.model_validate(prop)


@router.put("/{property_id}", response_model=PropertyResponse)
async def update_property(
    property_id: UUID,
    data: PropertyUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Update an existing property listing."""
    service = PropertyService(db)
    prop = await service.update(property_id, data)
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    return PropertyResponse.model_validate(prop)


@router.delete("/{property_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_property(
    property_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Delete a property listing."""
    service = PropertyService(db)
    deleted = await service.delete(property_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Property not found")

    # Also remove from vector store
    try:
        vector_service = VectorService()
        await vector_service.delete_property(str(property_id))
    except Exception:
        pass


@router.get("/market/stats")
async def get_market_stats(
    city: str | None = None,
    state: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    """Get aggregate market statistics."""
    service = PropertyService(db)
    return await service.get_market_stats(city=city, state=state)
