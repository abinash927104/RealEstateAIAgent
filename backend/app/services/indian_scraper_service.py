import logging
import urllib.parse
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

logger = logging.getLogger(__name__)

class MagicBricksScraperService:
    """Service to scrape live Indian property data from MagicBricks using Playwright."""

    async def search_properties(
        self, 
        city: str, 
        bedrooms: int = None, 
        max_price: int = None,
        limit: int = 5
    ) -> list[dict]:
        """Scrape properties from MagicBricks for a given city and criteria."""
        
        # Format city name for MagicBricks URL (e.g., "New Delhi" -> "New-Delhi")
        formatted_city = city.replace(" ", "-").title()
        
        # Construct the URL
        base_url = "https://www.magicbricks.com/property-for-sale/residential-real-estate"
        params = [
            f"cityName={urllib.parse.quote(formatted_city)}",
            "proptype=Multistory-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Residential-House,Villa"
        ]
        
        if bedrooms:
            params.append(f"bedroom={bedrooms}")
            
        # Magicbricks budget is typically &budgetMax=20000000
        if max_price:
            params.append(f"budgetMax={max_price}")

        search_url = f"{base_url}?{'&'.join(params)}"
        logger.info(f"Scraping MagicBricks URL: {search_url}")

        results = []
        
        try:
            async with async_playwright() as p:
                # Launch headless chromium
                browser = await p.chromium.launch(headless=True)
                # Create a context with a realistic user agent
                context = await browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                )
                page = await context.new_page()
                
                # Navigate to the page and wait for the property cards to load
                await page.goto(search_url, wait_until="domcontentloaded", timeout=30000)
                
                # MagicBricks can be slow, wait for the listing container
                try:
                    await page.wait_for_selector(".mb-srp__list", timeout=15000)
                except Exception:
                    logger.warning("Timeout waiting for .mb-srp__list, trying to parse anyway...")

                # Get the HTML content
                content = await page.content()
                await browser.close()

                # Parse with BeautifulSoup
                soup = BeautifulSoup(content, 'html.parser')
                
                # Find property cards
                cards = soup.find_all('div', class_='mb-srp__card')
                
                for card in cards[:limit]:
                    try:
                        # Extract Title
                        title_elem = card.find('h2', class_='mb-srp__card--title')
                        title = title_elem.text.strip() if title_elem else "Unknown Property"
                        
                        # Extract Price
                        price_elem = card.find('div', class_='mb-srp__card__price--amount')
                        price = price_elem.text.strip() if price_elem else "Price on Request"
                        
                        # Extract Carpet Area
                        area_elem = card.find('div', class_='mb-srp__card__summary--value', attrs={"data-summary": "carpet-area"})
                        area = area_elem.text.strip() if area_elem else "N/A"
                        
                        # Extract URL
                        link_elem = title_elem.find('a') if title_elem else None
                        url = link_elem['href'] if link_elem and 'href' in link_elem.attrs else search_url
                        
                        results.append({
                            "title": title,
                            "price": price,
                            "area": area,
                            "city": formatted_city,
                            "property_url": url,
                            "source": "MagicBricks"
                        })
                    except Exception as e:
                        logger.error(f"Error parsing a card: {e}")
                        continue
                        
        except Exception as e:
            logger.error(f"Scraping failed: {e}")
            return [{"error": f"Failed to scrape MagicBricks: {str(e)}"}]
            
        if not results:
            return [{"error": "No properties found or bot protection blocked the request."}]
            
        return results
