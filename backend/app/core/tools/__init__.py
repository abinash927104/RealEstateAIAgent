"""Tools package — register all agent tools here."""

from app.core.tools.property_search import property_search
from app.core.tools.mortgage_calc import mortgage_calculator
from app.core.tools.roi_analysis import roi_analysis
from app.core.tools.market_analysis import market_analysis

# All tools available to the AI agent
ALL_TOOLS = [
    property_search,
    mortgage_calculator,
    roi_analysis,
    market_analysis,
]

__all__ = [
    "property_search",
    "mortgage_calculator",
    "roi_analysis",
    "market_analysis",
    "ALL_TOOLS",
]
