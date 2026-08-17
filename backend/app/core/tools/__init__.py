"""Tools package — register all agent tools here."""

from app.core.tools.property_search import property_search
from app.core.tools.mortgage_calc import mortgage_calculator
from app.core.tools.roi_analysis import roi_analysis
from app.core.tools.market_analysis import market_analysis
from app.core.tools.real_api_search import SearchLivePropertiesTool
from app.core.tools.indian_api_search import SearchLiveIndianPropertiesTool
from app.core.tools.update_context import update_financial_context

search_live_properties = SearchLivePropertiesTool()
search_live_indian_properties = SearchLiveIndianPropertiesTool()

# All tools available to the AI agent
ALL_TOOLS = [
    property_search,
    search_live_properties,
    search_live_indian_properties,
    mortgage_calculator,
    roi_analysis,
    market_analysis,
    update_financial_context,
]

__all__ = [
    "property_search",
    "search_live_properties",
    "search_live_indian_properties",
    "mortgage_calculator",
    "roi_analysis",
    "market_analysis",
    "ALL_TOOLS",
]
