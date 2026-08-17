import asyncio
from app.services.indian_scraper_service import MagicBricksScraperService

async def test():
    print("Initializing MagicBricks scraper...")
    service = MagicBricksScraperService()
    res = await service.search_properties("Bangalore", limit=3)
    print("Results:", res)

asyncio.run(test())
