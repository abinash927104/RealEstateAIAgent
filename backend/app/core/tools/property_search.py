"""Property Search tool — queries the database for matching properties."""

from langchain_core.tools import tool
from pydantic import BaseModel, Field


class PropertySearchInput(BaseModel):
    """Input for the property search tool."""
    city: str | None = Field(None, description="City to search in (e.g., 'Austin', 'Miami')")
    state: str | None = Field(None, description="State abbreviation or full name (e.g., 'TX', 'Florida')")
    min_price: float | None = Field(None, description="Minimum property price in USD")
    max_price: float | None = Field(None, description="Maximum property price in USD")
    bedrooms: int | None = Field(None, description="Minimum number of bedrooms")
    bathrooms: int | None = Field(None, description="Minimum number of bathrooms")
    property_type: str | None = Field(None, description="Type: house, apartment, condo, townhouse, land, commercial")
    min_area_sqft: float | None = Field(None, description="Minimum area in square feet")
    query: str | None = Field(None, description="Natural language description for semantic search")


@tool(args_schema=PropertySearchInput)
async def property_search(
    city: str | None = None,
    state: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    bedrooms: int | None = None,
    bathrooms: int | None = None,
    property_type: str | None = None,
    min_area_sqft: float | None = None,
    query: str | None = None,
) -> str:
    """
    Search for real estate properties based on location, price, features, and natural language queries.
    Use this tool when the user wants to find properties, listings, or homes matching specific criteria.
    """
    from app.db.session import async_session_factory
    from app.services.property_service import PropertyService
    from app.services.vector_service import VectorService
    from app.schemas.property import PropertySearch

    results = []

    # Database structured search
    async with async_session_factory() as db:
        service = PropertyService(db)
        search_params = PropertySearch(
            city=city,
            state=state,
            min_price=min_price,
            max_price=max_price,
            min_bedrooms=bedrooms,
            min_bathrooms=bathrooms,
            property_type=property_type,
            min_area_sqft=min_area_sqft,
            page_size=10,
        )
        db_results = await service.search(search_params)
        for prop in db_results["properties"]:
            results.append({
                "id": str(prop.id),
                "title": prop.title,
                "price": float(prop.price),
                "bedrooms": prop.bedrooms,
                "bathrooms": prop.bathrooms,
                "area_sqft": prop.area_sqft,
                "address": prop.address,
                "city": prop.city,
                "state": prop.state,
                "property_type": prop.property_type.value if prop.property_type else None,
                "status": prop.status.value if prop.status else None,
                "images": prop.images[:2] if prop.images else [],
            })

    # Semantic search via ChromaDB if a natural language query is provided
    if query and not results:
        vector_service = VectorService()
        where_filter = {}
        if city:
            where_filter["city"] = city
        if property_type:
            where_filter["property_type"] = property_type

        semantic_results = await vector_service.search_properties(
            query=query,
            n_results=10,
            where=where_filter if where_filter else None,
        )
        for r in semantic_results:
            results.append({
                "id": r["id"],
                "description": r["document"],
                "metadata": r["metadata"],
                "relevance_score": round(1 - r["distance"], 3),
            })

    if not results:
        return "No properties found matching your criteria. Try broadening your search."

    # Format results
    output_lines = [f"Found {len(results)} properties:\n"]
    for i, prop in enumerate(results, 1):
        if "title" in prop:
            line = f"{i}. **{prop['title']}** — ${prop['price']:,.0f}"
            if prop.get("bedrooms"):
                line += f" | {prop['bedrooms']}bd/{prop.get('bathrooms', '?')}ba"
            if prop.get("area_sqft"):
                line += f" | {prop['area_sqft']:,.0f} sqft"
            line += f"\n   📍 {prop['address']}, {prop['city']}, {prop['state']}"
        else:
            line = f"{i}. {prop.get('description', 'Property')} (relevance: {prop.get('relevance_score', 'N/A')})"
        output_lines.append(line)

    return "\n".join(output_lines)
