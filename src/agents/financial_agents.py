"""Financial advisory agents."""
from langchain_anthropic import ChatAnthropic
from langchain.tools import tool
from src.tools.financial_tools import (
    calculate_retirement_needs,
    calculate_portfolio_allocation,
    calculate_emergency_fund,
    assess_debt_to_income_ratio,
    calculate_savings_rate,
    estimate_retirement_income
)


@tool
def analyze_retirement_needs(
    current_age: int,
    retirement_age: int,
    annual_expenses: float
) -> dict:
    """Analyze retirement savings needs based on user profile."""
    needed = calculate_retirement_needs(current_age, retirement_age, annual_expenses)
    return {
        "total_needed": needed,
        "years_to_retirement": retirement_age - current_age,
        "annual_requirement": annual_expenses
    }


@tool
def get_portfolio_recommendation(
    annual_income: float,
    risk_tolerance: str,
    years_to_goal: int
) -> dict:
    """Get portfolio allocation recommendation."""
    allocation = calculate_portfolio_allocation(annual_income, risk_tolerance, years_to_goal)
    return {
        "allocation": allocation,
        "risk_tolerance": risk_tolerance,
        "recommended_rebalance": "quarterly"
    }


@tool
def assess_financial_health(
    annual_income: float,
    monthly_expenses: float,
    monthly_debt: float,
    current_savings: float
) -> dict:
    """Assess overall financial health."""
    emergency_fund = calculate_emergency_fund(monthly_expenses)
    dti = assess_debt_to_income_ratio(annual_income, monthly_debt)
    savings = calculate_savings_rate(annual_income, monthly_expenses * 12)

    return {
        "emergency_fund_target": emergency_fund,
        "debt_to_income": dti,
        "savings_rate": savings,
        "current_savings": current_savings,
        "emergency_fund_status": "adequate" if current_savings >= emergency_fund else "needs improvement"
    }


@tool
def project_retirement_income(
    current_savings: float,
    annual_contribution: float,
    years_to_retirement: int,
    expected_return: float = 0.07
) -> dict:
    """Project retirement income potential."""
    projection = estimate_retirement_income(
        current_savings,
        annual_contribution,
        years_to_retirement,
        expected_return
    )
    return projection


def create_portfolio_agent():
    """Create portfolio analysis agent."""
    llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")
    tools = [get_portfolio_recommendation, assess_financial_health]
    return llm.bind_tools(tools)


def create_retirement_agent():
    """Create retirement planning agent."""
    llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")
    tools = [analyze_retirement_needs, project_retirement_income]
    return llm.bind_tools(tools)


def create_risk_assessment_agent():
    """Create risk assessment agent."""
    llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")
    tools = [assess_financial_health]
    return llm.bind_tools(tools)
