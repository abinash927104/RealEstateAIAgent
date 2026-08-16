"""Property service — CRUD and search operations for real estate listings."""

import math
import uuid

from sqlalchemy import select, func, and_, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.property import Property, PropertyStatus
from app.schemas.property import PropertyCreate, PropertyUpdate, PropertySearch


class PropertyService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, property_id: uuid.UUID) -> Property | None:
        result = await self.db.execute(select(Property).where(Property.id == property_id))
        return result.scalar_one_or_none()

    async def create(self, data: PropertyCreate, owner_id: uuid.UUID | None = None) -> Property:
        prop = Property(
            **data.model_dump(),
            owner_id=owner_id,
        )
        self.db.add(prop)
        await self.db.flush()
        await self.db.refresh(prop)
        return prop

    async def update(self, property_id: uuid.UUID, data: PropertyUpdate) -> Property | None:
        prop = await self.get_by_id(property_id)
        if not prop:
            return None
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(prop, field, value)
        await self.db.flush()
        await self.db.refresh(prop)
        return prop

    async def delete(self, property_id: uuid.UUID) -> bool:
        prop = await self.get_by_id(property_id)
        if not prop:
            return False
        await self.db.delete(prop)
        await self.db.flush()
        return True

    async def search(self, params: PropertySearch) -> dict:
        """Search properties with filters, pagination, and sorting."""
        query = select(Property)
        count_query = select(func.count(Property.id))
        conditions = []

        # Apply filters
        if params.city:
            conditions.append(Property.city.ilike(f"%{params.city}%"))
        if params.state:
            conditions.append(Property.state.ilike(f"%{params.state}%"))
        if params.zip_code:
            conditions.append(Property.zip_code == params.zip_code)
        if params.property_type:
            conditions.append(Property.property_type == params.property_type)
        if params.min_price is not None:
            conditions.append(Property.price >= params.min_price)
        if params.max_price is not None:
            conditions.append(Property.price <= params.max_price)
        if params.min_bedrooms is not None:
            conditions.append(Property.bedrooms >= params.min_bedrooms)
        if params.max_bedrooms is not None:
            conditions.append(Property.bedrooms <= params.max_bedrooms)
        if params.min_bathrooms is not None:
            conditions.append(Property.bathrooms >= params.min_bathrooms)
        if params.min_area_sqft is not None:
            conditions.append(Property.area_sqft >= params.min_area_sqft)
        if params.max_area_sqft is not None:
            conditions.append(Property.area_sqft <= params.max_area_sqft)
        if params.status:
            conditions.append(Property.status == params.status)

        if conditions:
            query = query.where(and_(*conditions))
            count_query = count_query.where(and_(*conditions))

        # Get total count
        total_result = await self.db.execute(count_query)
        total = total_result.scalar()

        # Sorting
        sort_column = getattr(Property, params.sort_by, Property.listed_at)
        order_func = desc if params.sort_order == "desc" else asc
        query = query.order_by(order_func(sort_column))

        # Pagination
        offset = (params.page - 1) * params.page_size
        query = query.offset(offset).limit(params.page_size)

        result = await self.db.execute(query)
        properties = result.scalars().all()

        return {
            "properties": properties,
            "total": total,
            "page": params.page,
            "page_size": params.page_size,
            "total_pages": math.ceil(total / params.page_size) if total > 0 else 0,
        }

    async def get_market_stats(self, city: str | None = None, state: str | None = None) -> dict:
        """Get aggregate market statistics for a location."""
        query = select(
            func.count(Property.id).label("total_listings"),
            func.avg(Property.price).label("avg_price"),
            func.min(Property.price).label("min_price"),
            func.max(Property.price).label("max_price"),
            func.avg(Property.area_sqft).label("avg_sqft"),
            func.avg(Property.price / func.nullif(Property.area_sqft, 0)).label("avg_price_per_sqft"),
        ).where(Property.status == PropertyStatus.ACTIVE)

        if city:
            query = query.where(Property.city.ilike(f"%{city}%"))
        if state:
            query = query.where(Property.state.ilike(f"%{state}%"))

        result = await self.db.execute(query)
        row = result.one()

        return {
            "total_listings": row.total_listings or 0,
            "avg_price": round(float(row.avg_price or 0), 2),
            "min_price": float(row.min_price or 0),
            "max_price": float(row.max_price or 0),
            "avg_sqft": round(float(row.avg_sqft or 0), 0),
            "avg_price_per_sqft": round(float(row.avg_price_per_sqft or 0), 2),
        }
