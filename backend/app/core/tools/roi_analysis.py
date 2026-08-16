"""ROI Analysis tool — investment return calculations for rental properties."""

from langchain_core.tools import tool
from pydantic import BaseModel, Field


class ROIInput(BaseModel):
    """Input for ROI analysis."""
    purchase_price: float = Field(..., description="Property purchase price in USD")
    down_payment_percent: float = Field(20.0, description="Down payment percentage")
    monthly_rent: float = Field(..., description="Expected monthly rental income in USD")
    annual_interest_rate: float = Field(6.5, description="Mortgage interest rate percentage")
    loan_term_years: int = Field(30, description="Loan term in years")
    annual_property_tax_rate: float = Field(1.2, description="Property tax rate percentage")
    annual_insurance: float = Field(1500.0, description="Annual insurance cost in USD")
    monthly_hoa: float = Field(0.0, description="Monthly HOA fees in USD")
    annual_maintenance_rate: float = Field(1.0, description="Annual maintenance cost as percentage of property value")
    vacancy_rate: float = Field(5.0, description="Expected vacancy rate as percentage")
    annual_appreciation_rate: float = Field(3.0, description="Expected annual property appreciation percentage")


@tool(args_schema=ROIInput)
async def roi_analysis(
    purchase_price: float,
    down_payment_percent: float = 20.0,
    monthly_rent: float = 0.0,
    annual_interest_rate: float = 6.5,
    loan_term_years: int = 30,
    annual_property_tax_rate: float = 1.2,
    annual_insurance: float = 1500.0,
    monthly_hoa: float = 0.0,
    annual_maintenance_rate: float = 1.0,
    vacancy_rate: float = 5.0,
    annual_appreciation_rate: float = 3.0,
) -> str:
    """
    Analyze the return on investment for a rental property.
    Use this when the user asks about investment potential, cap rates, cash-on-cash returns,
    or whether a property is a good investment.
    """
    # Capital invested
    down_payment = purchase_price * (down_payment_percent / 100)
    closing_costs = purchase_price * 0.03  # Estimate 3% closing costs
    total_investment = down_payment + closing_costs

    # Mortgage calculation
    loan_amount = purchase_price - down_payment
    monthly_rate = (annual_interest_rate / 100) / 12
    num_payments = loan_term_years * 12

    if monthly_rate > 0 and loan_amount > 0:
        monthly_mortgage = loan_amount * (
            (monthly_rate * (1 + monthly_rate) ** num_payments)
            / ((1 + monthly_rate) ** num_payments - 1)
        )
    else:
        monthly_mortgage = loan_amount / num_payments if num_payments > 0 else 0

    # Monthly expenses
    monthly_tax = (purchase_price * (annual_property_tax_rate / 100)) / 12
    monthly_insurance = annual_insurance / 12
    monthly_maintenance = (purchase_price * (annual_maintenance_rate / 100)) / 12
    vacancy_cost = monthly_rent * (vacancy_rate / 100)

    total_monthly_expenses = (
        monthly_mortgage + monthly_tax + monthly_insurance
        + monthly_maintenance + monthly_hoa + vacancy_cost
    )

    # Cash flow
    effective_rent = monthly_rent * (1 - vacancy_rate / 100)
    monthly_cash_flow = effective_rent - total_monthly_expenses + vacancy_cost  # vacancy already in expenses
    monthly_cash_flow = monthly_rent - total_monthly_expenses
    annual_cash_flow = monthly_cash_flow * 12

    # NOI (Net Operating Income) — excludes mortgage
    annual_operating_expenses = (
        (monthly_tax + monthly_insurance + monthly_maintenance + monthly_hoa + vacancy_cost) * 12
    )
    annual_gross_income = monthly_rent * 12
    noi = annual_gross_income - annual_operating_expenses

    # Key metrics
    cap_rate = (noi / purchase_price) * 100 if purchase_price > 0 else 0
    cash_on_cash = (annual_cash_flow / total_investment) * 100 if total_investment > 0 else 0
    gross_yield = (annual_gross_income / purchase_price) * 100 if purchase_price > 0 else 0

    # Break-even
    if monthly_cash_flow > 0:
        break_even_months = total_investment / monthly_cash_flow
        break_even_years = break_even_months / 12
    else:
        break_even_months = float("inf")
        break_even_years = float("inf")

    # 5-year projection with appreciation
    projected_value_5yr = purchase_price * ((1 + annual_appreciation_rate / 100) ** 5)
    equity_gain_5yr = projected_value_5yr - purchase_price
    total_cash_flow_5yr = annual_cash_flow * 5
    total_return_5yr = equity_gain_5yr + total_cash_flow_5yr
    total_roi_5yr = (total_return_5yr / total_investment) * 100 if total_investment > 0 else 0

    # Investment grade
    if cap_rate >= 8:
        grade = "🟢 A (Excellent)"
    elif cap_rate >= 6:
        grade = "🟢 B (Good)"
    elif cap_rate >= 4:
        grade = "🟡 C (Average)"
    elif cap_rate >= 2:
        grade = "🟠 D (Below Average)"
    else:
        grade = "🔴 F (Poor)"

    break_even_str = f"{break_even_years:.1f} years" if break_even_years < 100 else "N/A (negative cash flow)"

    return f"""
📈 **Investment ROI Analysis**

**Investment Grade: {grade}**

| Metric | Value |
|--------|-------|
| **Purchase Price** | ${purchase_price:,.2f} |
| **Down Payment** ({down_payment_percent:.0f}%) | ${down_payment:,.2f} |
| **Closing Costs** (~3%) | ${closing_costs:,.2f} |
| **Total Cash Invested** | ${total_investment:,.2f} |

**Monthly Cash Flow:**

| Item | Amount |
|------|--------|
| Rental Income | ${monthly_rent:,.2f} |
| Mortgage Payment | -${monthly_mortgage:,.2f} |
| Property Tax | -${monthly_tax:,.2f} |
| Insurance | -${monthly_insurance:,.2f} |
| Maintenance | -${monthly_maintenance:,.2f} |
| HOA | -${monthly_hoa:,.2f} |
| Vacancy Reserve | -${vacancy_cost:,.2f} |
| **Net Cash Flow** | **${monthly_cash_flow:,.2f}** |

**Key Investment Metrics:**

| Metric | Value |
|--------|-------|
| Cap Rate | {cap_rate:.2f}% |
| Cash-on-Cash Return | {cash_on_cash:.2f}% |
| Gross Yield | {gross_yield:.2f}% |
| Annual NOI | ${noi:,.2f} |
| Annual Cash Flow | ${annual_cash_flow:,.2f} |
| Break-Even | {break_even_str} |

**5-Year Projection** (at {annual_appreciation_rate:.1f}% annual appreciation):
- Projected Property Value: ${projected_value_5yr:,.2f}
- Equity Gain: ${equity_gain_5yr:,.2f}
- Total Cash Flow: ${total_cash_flow_5yr:,.2f}
- **Total 5-Year ROI: {total_roi_5yr:.1f}%**
"""
