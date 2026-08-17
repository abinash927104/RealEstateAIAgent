import asyncio
from app.services.rapidapi_service import RapidAPIService

async def test():
    service = RapidAPIService()
    res = await service.search_properties("Seattle", "WA", limit=2)
    print(res)

asyncio.run(test())
