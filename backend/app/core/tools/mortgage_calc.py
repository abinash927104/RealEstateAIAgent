"""Mortgage Calculator tool — deterministic financial calculations."""

from langchain_core.tools import tool
from pydantic import BaseModel, Field


class MortgageInput(BaseModel):
    """Input for the mortgage calculator."""
    property_price: float = Field(..., description="Total property price (parse text like '1.5 Cr' into 15000000.0 before passing)")
    down_payment_percent: float = Field(20.0, description="Down payment as a percentage (e.g., 20 for 20%)")
    annual_interest_rate: float = Field(8.5, description="Annual interest rate as a percentage (e.g., 8.5 for 8.5%)")
    loan_term_years: int = Field(20, description="Loan term in years (typically 15, 20 or 30)")
    annual_property_tax_rate: float = Field(1.2, description="Annual property tax rate as percentage of home value")
    annual_insurance: float = Field(1500.0, description="Annual homeowners insurance")
    monthly_hoa: float = Field(0.0, description="Monthly HOA fees")
    currency_symbol: str = Field("$", description="Currency symbol to use in the output (e.g., '$', '₹')")


@tool(args_schema=MortgageInput)
async def mortgage_calculator(
    property_price: float,
    down_payment_percent: float = 20.0,
    annual_interest_rate: float = 8.5,
    loan_term_years: int = 20,
    annual_property_tax_rate: float = 1.2,
    annual_insurance: float = 1500.0,
    monthly_hoa: float = 0.0,
    currency_symbol: str = "$",
) -> str:
    """
    Calculate monthly mortgage payments with a detailed breakdown.
    Use this when the user asks about mortgage payments, EMI, affordability, or wants to know how much
    a property will cost per month. Uses deterministic math — never estimates.
    """
    # Core calculations
    down_payment = property_price * (down_payment_percent / 100)
    loan_amount = property_price - down_payment
    monthly_rate = (annual_interest_rate / 100) / 12
    num_payments = loan_term_years * 12

    # Monthly principal & interest (amortization formula)
    if monthly_rate > 0:
        monthly_pi = loan_amount * (
            (monthly_rate * (1 + monthly_rate) ** num_payments)
            / ((1 + monthly_rate) ** num_payments - 1)
        )
    else:
        monthly_pi = loan_amount / num_payments

    # Monthly property tax
    monthly_tax = (property_price * (annual_property_tax_rate / 100)) / 12

    # Monthly insurance
    monthly_insurance = annual_insurance / 12

    # Total monthly payment
    total_monthly = monthly_pi + monthly_tax + monthly_insurance + monthly_hoa

    # Total cost over loan lifetime
    total_interest = (monthly_pi * num_payments) - loan_amount
    total_cost = monthly_pi * num_payments + (monthly_tax + monthly_insurance + monthly_hoa) * num_payments

    c = currency_symbol
    return f"""
📊 **Mortgage Payment Breakdown**

| Item | Amount |
|------|--------|
| **Property Price** | {c}{property_price:,.2f} |
| **Down Payment** ({down_payment_percent:.1f}%) | {c}{down_payment:,.2f} |
| **Loan Amount** | {c}{loan_amount:,.2f} |
| **Interest Rate** | {annual_interest_rate:.2f}% |
| **Loan Term** | {loan_term_years} years |

**Monthly EMI (Principal + Interest): {c}{monthly_pi:,.2f}**

| Component | Monthly |
|-----------|---------|
| EMI (P&I) | {c}{monthly_pi:,.2f} |
| Property Tax | {c}{monthly_tax:,.2f} |
| Insurance | {c}{monthly_insurance:,.2f} |
| HOA Fees | {c}{monthly_hoa:,.2f} |
| **Total** | **{c}{total_monthly:,.2f}** |

**Lifetime Costs:**
- Total Interest Paid: {c}{total_interest:,.2f}
- Total Cost over {loan_term_years} years: {c}{total_cost:,.2f}
"""
