"""Market Analysis tool — aggregate market statistics and trends."""

from langchain_core.tools import tool
from pydantic import BaseModel, Field


class MarketAnalysisInput(BaseModel):
    """Input for market analysis."""
    city: str = Field(..., description="City name to analyze")
    state: str | None = Field(None, description="State name or abbreviation")
    property_type: str | None = Field(None, description="Property type to focus on")


@tool(args_schema=MarketAnalysisInput)
async def market_analysis(
    city: str,
    state: str | None = None,
    property_type: str | None = None,
) -> str:
    """
    Analyze the real estate market for a specific city/area.
    Use this when the user asks about market conditions, trends, average prices,
    or wants to compare markets. Provides data from the local database.
    """
    from app.db.session import async_session_factory
    from app.services.property_service import PropertyService
    from app.models.property import Property, PropertyStatus, PropertyType
    from sqlalchemy import select, func

    async with async_session_factory() as db:
        service = PropertyService(db)
        stats = await service.get_market_stats(city=city, state=state)

        # Get property type distribution
        type_query = (
            select(
                Property.property_type,
                func.count(Property.id).label("count"),
                func.avg(Property.price).label("avg_price"),
            )
            .where(Property.status == PropertyStatus.ACTIVE)
            .where(Property.city.ilike(f"%{city}%"))
        )
        if state:
            type_query = type_query.where(Property.state.ilike(f"%{state}%"))
        type_query = type_query.group_by(Property.property_type)

        result = await db.execute(type_query)
        type_dist = result.all()

        # Get price range distribution
        price_ranges = []
        for label, min_p, max_p in [
            ("Under $200K", 0, 200000),
            ("$200K - $400K", 200000, 400000),
            ("$400K - $600K", 400000, 600000),
            ("$600K - $800K", 600000, 800000),
            ("$800K - $1M", 800000, 1000000),
            ("Over $1M", 1000000, 999999999),
        ]:
            count_q = (
                select(func.count(Property.id))
                .where(Property.status == PropertyStatus.ACTIVE)
                .where(Property.city.ilike(f"%{city}%"))
                .where(Property.price >= min_p)
                .where(Property.price < max_p)
            )
            if state:
                count_q = count_q.where(Property.state.ilike(f"%{state}%"))
            count_result = await db.execute(count_q)
            count = count_result.scalar()
            if count and count > 0:
                price_ranges.append(f"  - {label}: {count} listings")

    # Format output
    state_str = f", {state}" if state else ""
    type_lines = []
    for row in type_dist:
        ptype = row[0].value if row[0] else "Unknown"
        count = row[1]
        avg_p = float(row[2]) if row[2] else 0
        type_lines.append(f"  - {ptype.title()}: {count} listings (avg ${avg_p:,.0f})")

    return f"""
🏘️ **Market Analysis: {city}{state_str}**

**Market Overview:**

| Metric | Value |
|--------|-------|
| Total Active Listings | {stats['total_listings']} |
| Average Price | ${stats['avg_price']:,.2f} |
| Price Range | ${stats['min_price']:,.0f} — ${stats['max_price']:,.0f} |
| Average Size | {stats['avg_sqft']:,.0f} sqft |
| Avg Price/sqft | ${stats['avg_price_per_sqft']:,.2f} |

**Property Type Distribution:**
{chr(10).join(type_lines) if type_lines else '  No data available'}

**Price Range Distribution:**
{chr(10).join(price_ranges) if price_ranges else '  No data available'}

> 💡 *Data sourced from local database listings. For the most up-to-date market trends, consider checking Zillow or Redfin.*
"""
