"""Favorites API routes."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.favorite import Favorite
from app.schemas.property import PropertyResponse
from app.utils.auth import get_current_user

router = APIRouter(prefix="/favorites", tags=["Favorites"])


class FavoriteCreate(BaseModel):
    property_id: UUID
    notes: str | None = None


class FavoriteResponse(BaseModel):
    id: UUID
    property_id: UUID
    notes: str | None
    created_at: str

    model_config = {"from_attributes": True}


@router.get("")
async def list_favorites(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """List all favorited properties for the current user."""
    result = await db.execute(
        select(Favorite)
        .where(Favorite.user_id == current_user.id)
        .order_by(Favorite.created_at.desc())
    )
    favorites = result.scalars().all()

    return [
        {
            "id": str(f.id),
            "property_id": str(f.property_id),
            "notes": f.notes,
            "created_at": f.created_at.isoformat(),
            "property": PropertyResponse.model_validate(f.property) if f.property else None,
        }
        for f in favorites
    ]


@router.post("", status_code=status.HTTP_201_CREATED)
async def add_favorite(
    data: FavoriteCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Add a property to favorites."""
    # Check for duplicate
    existing = await db.execute(
        select(Favorite).where(
            Favorite.user_id == current_user.id,
            Favorite.property_id == data.property_id,
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Property already in favorites")

    favorite = Favorite(
        user_id=current_user.id,
        property_id=data.property_id,
        notes=data.notes,
    )
    db.add(favorite)
    await db.flush()
    await db.refresh(favorite)

    return {"id": str(favorite.id), "message": "Property added to favorites"}


@router.delete("/{favorite_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_favorite(
    favorite_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Remove a property from favorites."""
    result = await db.execute(
        select(Favorite).where(
            Favorite.id == favorite_id,
            Favorite.user_id == current_user.id,
        )
    )
    favorite = result.scalar_one_or_none()
    if not favorite:
        raise HTTPException(status_code=404, detail="Favorite not found")
    await db.delete(favorite)
    await db.flush()
