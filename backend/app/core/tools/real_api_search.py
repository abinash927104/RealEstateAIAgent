import json
import logging
from typing import Optional, Type

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from app.services.rapidapi_service import RapidAPIService

logger = logging.getLogger(__name__)

class SearchLivePropertiesInput(BaseModel):
    """Input for SearchLivePropertiesTool."""
    location: str = Field(description="City name to search in (e.g. 'Seattle')")
    state_code: str = Field(description="2-letter state code (e.g. 'WA')")
    limit: int = Field(default=5, description="Number of results to return (max 10)")
    min_price: Optional[int] = Field(default=None, description="Minimum price in USD")
    max_price: Optional[int] = Field(default=None, description="Maximum price in USD")
    beds_min: Optional[int] = Field(default=None, description="Minimum number of bedrooms")


class SearchLivePropertiesTool(BaseTool):
    """Tool to search for real, live properties using RapidAPI (e.g. Zillow/Realtor data)."""
    
    name: str = "search_live_properties"
    description: str = (
        "Use this tool when the user asks to find REAL, LIVE, or ZILLOW/REALTOR properties on the market. "
        "Do NOT use this tool for general database queries unless the user specifically asks for live or real-time data."
    )
    args_schema: Type[BaseModel] = SearchLivePropertiesInput
    
    def _run(self, *args, **kwargs) -> str:
        """Sync execution is not supported."""
        raise NotImplementedError("Use _arun instead")

    async def _arun(
        self,
        location: str,
        state_code: str,
        limit: int = 5,
        min_price: Optional[int] = None,
        max_price: Optional[int] = None,
        beds_min: Optional[int] = None,
    ) -> str:
        """Execute the live property search asynchronously."""
        try:
            service = RapidAPIService()
            results = await service.search_properties(
                location=location,
                state_code=state_code,
                limit=limit,
                min_price=min_price,
                max_price=max_price,
                beds_min=beds_min
            )
            
            if not results:
                return f"No live properties found in {location}, {state_code} matching your criteria."
                
            if "error" in results[0]:
                return f"API Error: {results[0]['error']}"
                
            # Format results for the LLM
            formatted = f"Found {len(results)} live properties in {location}, {state_code}:\n\n"
            for p in results:
                formatted += (
                    f"- **{p['address']}, {p['city']}, {p['state']}**\n"
                    f"  Price: ${p['price']:,.2f} | Beds: {p['bedrooms']} | Baths: {p['bathrooms']} | Sqft: {p['sqft']}\n"
                    f"  Status: {p['status']}\n"
                )
                if p.get('property_url'):
                    formatted += f"  Link: [View on Realtor]({p['property_url']})\n"
                formatted += "\n"
                
            return formatted

        except Exception as e:
            logger.error(f"Error in SearchLivePropertiesTool: {e}")
            return f"Failed to search live properties: {str(e)}"
