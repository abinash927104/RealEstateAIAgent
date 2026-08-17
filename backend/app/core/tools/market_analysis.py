"""Market Analysis tool — aggregate market statistics and trends."""

from langchain_core.tools import tool
from pydantic import BaseModel, Field


class MarketAnalysisInput(BaseModel):
    """Input for market analysis."""
    city: str = Field(..., description="City name to analyze")
    state: str | None = Field(None, description="State name or abbreviation")
    property_type: str | None = Field(None, description="Property type to focus on")
    currency_symbol: str = Field("$", description="Currency symbol to use in the output (e.g., '$', '₹')")


def parse_indian_price(price_str: str) -> float:
    """Helper to parse Indian prices like '₹17 Cr' or '93 Lac' to float."""
    import re
    cleaned = price_str.replace("₹", "").replace(",", "").strip()
    match = re.search(r"([\d\.]+)", cleaned)
    if not match:
        return 0.0
    val = float(match.group(1))
    lower_str = cleaned.lower()
    if "cr" in lower_str:
        return val * 10000000
    elif "lac" in lower_str or "lakh" in lower_str:
        return val * 100000
    return val


@tool(args_schema=MarketAnalysisInput)
async def market_analysis(
    city: str,
    state: str | None = None,
    property_type: str | None = None,
    currency_symbol: str = "$",
) -> str:
    """
    Analyze the real estate market for a specific city/area.
    Use this when the user asks about market conditions, trends, average prices,
    or wants to compare markets. Will use local data or live scraping automatically.
    """
    from app.db.session import async_session_factory
    from app.services.property_service import PropertyService
    from app.models.property import Property, PropertyStatus
    from sqlalchemy import select, func

    async with async_session_factory() as db:
        service = PropertyService(db)
        stats = await service.get_market_stats(city=city, state=state)

        total_listings = stats.get('total_listings', 0)
        
        # If no listings in local DB and user is asking for an Indian city (inferred via ₹ or just try scraping anyway)
        if total_listings == 0:
            from app.services.indian_scraper_service import MagicBricksScraperService
            scraper = MagicBricksScraperService()
            # Scrape up to 15 properties to generate a dynamic market report
            live_props = await scraper.search_properties(city=city, limit=15)
            
            if not live_props or "error" in live_props[0]:
                return f"Sorry, no local data found for {city} and live scraping failed."
                
            prices = []
            for p in live_props:
                val = parse_indian_price(p.get("price", ""))
                if val > 0:
                    prices.append(val)
            
            if not prices:
                return f"Sorry, couldn't extract reliable pricing data for {city} from live listings."
                
            avg_price = sum(prices) / len(prices)
            min_price = min(prices)
            max_price = max(prices)
            
            c = currency_symbol
            return f"""
🏘️ **Live Market Analysis: {city} (via MagicBricks Scraper)**

**Market Overview (Based on {len(live_props)} recent live listings):**

| Metric | Value |
|--------|-------|
| Average Price | {c}{avg_price:,.2f} |
| Price Range | {c}{min_price:,.0f} — {c}{max_price:,.0f} |
| Sample Size | {len(live_props)} active listings |

> 💡 *Data dynamically scraped from live MagicBricks listings because local database had 0 properties.*
"""

        # Local DB Path
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
            ("Under 20L", 0, 2000000),
            ("20L - 50L", 2000000, 5000000),
            ("50L - 1Cr", 5000000, 10000000),
            ("1Cr - 5Cr", 10000000, 50000000),
            ("Over 5Cr", 50000000, 9999999999),
        ] if currency_symbol == "₹" else [
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
    c = currency_symbol
    state_str = f", {state}" if state else ""
    type_lines = []
    for row in type_dist:
        ptype = row[0].value if row[0] else "Unknown"
        count = row[1]
        avg_p = float(row[2]) if row[2] else 0
        type_lines.append(f"  - {ptype.title()}: {count} listings (avg {c}{avg_p:,.0f})")

    return f"""
🏘️ **Market Analysis: {city}{state_str}**

**Market Overview (Based on {total_listings} local listings):**

| Metric | Value |
|--------|-------|
| Total Active Listings | {stats['total_listings']} |
| Average Price | {c}{stats['avg_price']:,.2f} |
| Price Range | {c}{stats['min_price']:,.0f} — {c}{stats['max_price']:,.0f} |
| Average Size | {stats['avg_sqft']:,.0f} sqft |
| Avg Price/sqft | {c}{stats['avg_price_per_sqft']:,.2f} |

**Property Type Distribution:**
{chr(10).join(type_lines) if type_lines else '  No data available'}

**Price Range Distribution:**
{chr(10).join(price_ranges) if price_ranges else '  No data available'}

> 💡 *Note: This analysis is based strictly on the {total_listings} properties in our current dataset. For broader or more live market trends, consider checking MagicBricks or Zillow.*
"""
