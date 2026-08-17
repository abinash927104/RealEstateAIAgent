import logging
from typing import Optional, Type

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from app.services.indian_scraper_service import MagicBricksScraperService

logger = logging.getLogger(__name__)

class SearchLiveIndianPropertiesInput(BaseModel):
    """Input for SearchLiveIndianPropertiesTool."""
    city: str = Field(description="City name in India to search in (e.g. 'Bangalore', 'Mumbai')")
    bedrooms: Optional[int] = Field(default=None, description="Number of bedrooms (e.g. 2, 3)")
    max_price: Optional[int] = Field(default=None, description="Maximum price in INR")
    limit: int = Field(default=5, description="Number of results to return")

class SearchLiveIndianPropertiesTool(BaseTool):
    """Tool to search for real, live Indian properties by scraping MagicBricks."""
    
    name: str = "search_live_indian_properties"
    description: str = (
        "Use this tool to find REAL, LIVE properties in Indian cities (like Bangalore, Mumbai, Delhi) "
        "by scraping Indian real estate portals like MagicBricks. "
        "Use this specifically when the user asks for properties in India and implies they want live market data."
    )
    args_schema: Type[BaseModel] = SearchLiveIndianPropertiesInput
    
    def _run(self, *args, **kwargs) -> str:
        raise NotImplementedError("Use _arun instead")

    async def _arun(
        self,
        city: str,
        bedrooms: Optional[int] = None,
        max_price: Optional[int] = None,
        limit: int = 5
    ) -> str:
        """Execute the live Indian property search asynchronously."""
        try:
            service = MagicBricksScraperService()
            results = await service.search_properties(
                city=city,
                bedrooms=bedrooms,
                max_price=max_price,
                limit=limit
            )
            
            if not results:
                return f"No live properties found in {city} matching your criteria."
                
            if "error" in results[0]:
                return f"Scraping Error: {results[0]['error']}"
                
            formatted = f"Found {len(results)} live Indian properties in {city} (via MagicBricks):\n\n"
            for p in results:
                formatted += (
                    f"- **{p['title']}**\n"
                    f"  Price: {p['price']} | Carpet Area: {p['area']}\n"
                )
                if p.get('property_url'):
                    formatted += f"  Link: [View on MagicBricks]({p['property_url']})\n"
                formatted += "\n"
                
            return formatted

        except Exception as e:
            logger.error(f"Error in SearchLiveIndianPropertiesTool: {e}")
            return f"Failed to search live Indian properties: {str(e)}"
