import logging
import httpx
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

class RapidAPIService:
    """Service to interact with the RapidAPI Real Estate API (e.g. realty-in-us)."""
    
    def __init__(self):
        self.api_key = settings.RAPIDAPI_KEY
        self.api_host = settings.RAPIDAPI_HOST
        self.base_url = f"https://{self.api_host}"

    async def search_properties(
        self, 
        location: str, 
        state_code: str = "NY", 
        limit: int = 5,
        min_price: int = None,
        max_price: int = None,
        beds_min: int = None
    ) -> list[dict]:
        """
        Search for live properties using the RapidAPI endpoint.
        Falls back to a mock response if the API key is not configured.
        """
        if not self.api_key or self.api_key == "your-rapidapi-key":
            logger.warning("RapidAPI key is not configured. Returning mock live data.")
            return self._get_mock_data(location, limit)

        # Example endpoint for realty-in-us (Note: endpoints may vary based on the exact API used)
        endpoint = "/properties/v3/list"
        
        headers = {
            "x-rapidapi-key": self.api_key,
            "x-rapidapi-host": self.api_host
        }

        # Query parameters typically expected by the API
        params = {
            "city": location,
            "state_code": state_code,
            "limit": str(limit),
            "offset": "0",
            "sort": "relevance"
        }
        
        if min_price:
            params["price_min"] = str(min_price)
        if max_price:
            params["price_max"] = str(max_price)
        if beds_min:
            params["beds_min"] = str(beds_min)

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{self.base_url}{endpoint}", 
                    headers=headers, 
                    params=params
                )
                
                if response.status_code != 200:
                    logger.error(f"RapidAPI error {response.status_code}: {response.text}")
                    return [{"error": f"API Error: {response.status_code}. Make sure your RapidAPI key is valid and subscribed to {self.api_host}."}]

                data = response.json()
                
                # Parse the specific response structure of realty-in-us
                properties = data.get("data", {}).get("home_search", {}).get("results", [])
                
                if not properties:
                    # Fallback parsing in case the structure is different
                    properties = data.get("properties", data.get("results", []))
                    
                formatted_results = []
                for p in properties[:limit]:
                    loc = p.get("location", {})
                    address = loc.get("address", {})
                    
                    formatted_results.append({
                        "property_id": p.get("property_id", "N/A"),
                        "address": address.get("line", p.get("address", "N/A")),
                        "city": address.get("city", location),
                        "state": address.get("state_code", state_code),
                        "price": p.get("list_price", p.get("price", "N/A")),
                        "bedrooms": p.get("description", {}).get("beds", "N/A"),
                        "bathrooms": p.get("description", {}).get("baths", "N/A"),
                        "sqft": p.get("description", {}).get("sqft", "N/A"),
                        "property_url": f"https://www.realtor.com/realestateandhomes-detail/{p.get('permalink')}" if p.get("permalink") else None,
                        "status": p.get("status", "Active")
                    })
                    
                return formatted_results

        except Exception as e:
            logger.error(f"Failed to fetch properties from RapidAPI: {e}")
            return [{"error": f"Failed to connect to RapidAPI: {str(e)}"}]

    def _get_mock_data(self, location: str, limit: int) -> list[dict]:
        """Return some fake data so the AI can still demonstrate the capability if no key is present."""
        return [
            {
                "property_id": f"mock-{i}",
                "address": f"{100 + i} Live API Street",
                "city": location,
                "state": "NY",
                "price": 500000 + (i * 50000),
                "bedrooms": 3 + (i % 2),
                "bathrooms": 2,
                "sqft": 1500 + (i * 200),
                "property_url": "https://www.realtor.com/",
                "status": "Active (Mock Data - Configure RAPIDAPI_KEY for real results)"
            }
            for i in range(min(limit, 3))
        ]
