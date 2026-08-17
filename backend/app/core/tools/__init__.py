"""Tools package — register all agent tools here."""

from app.core.tools.property_search import property_search
from app.core.tools.mortgage_calc import mortgage_calculator
from app.core.tools.roi_analysis import roi_analysis
from app.core.tools.market_analysis import market_analysis
from app.core.tools.real_api_search import SearchLivePropertiesTool

search_live_properties = SearchLivePropertiesTool()

# All tools available to the AI agent
ALL_TOOLS = [
    property_search,
    search_live_properties,
    mortgage_calculator,
    roi_analysis,
    market_analysis,
]

__all__ = [
    "property_search",
    "search_live_properties",
    "mortgage_calculator",
    "roi_analysis",
    "market_analysis",
    "ALL_TOOLS",
]
