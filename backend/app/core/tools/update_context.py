"""Update Context tool — used by the agent to persist state across turns."""

from langchain_core.tools import tool
from pydantic import BaseModel, Field


class UpdateContextInput(BaseModel):
    """Input for updating the financial and search context."""
    city: str | None = Field(None, description="Current city")
    property_type: str | None = Field(None, description="Current property type constraint")
    min_price: float | None = Field(None, description="Current min price")
    max_price: float | None = Field(None, description="Current max price")
    purchase_price: float | None = Field(None, description="Current property purchase price")
    monthly_rent: float | None = Field(None, description="Current expected monthly rent")
    down_payment_percent: float | None = Field(None, description="Current down payment percentage")
    annual_interest_rate: float | None = Field(None, description="Current mortgage interest rate")
    loan_term_years: int | None = Field(None, description="Current loan term in years")


@tool(args_schema=UpdateContextInput)
async def update_financial_context(
    city: str | None = None,
    property_type: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    purchase_price: float | None = None,
    monthly_rent: float | None = None,
    down_payment_percent: float | None = None,
    annual_interest_rate: float | None = None,
    loan_term_years: int | None = None,
) -> str:
    """
    Update the conversational context with new financial or search parameters.
    Use this tool whenever the user changes an assumption (like rent, price, down payment, city) 
    so it is remembered for the rest of the conversation.
    """
    return "Context updated successfully."
