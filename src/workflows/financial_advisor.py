"""Main financial advisor workflow using LangGraph."""
from langgraph.graph import StateGraph, START, END
from langchain_anthropic import ChatAnthropic
from langchain.tools import tool
from typing import TypedDict, Any
import json

from src.models.financial import UserProfile, FinancialAnalysis
from src.tools.financial_tools import (
    calculate_retirement_needs,
    calculate_portfolio_allocation,
    assess_debt_to_income_ratio,
    estimate_retirement_income
)


class FinancialAdvisoryState(TypedDict):
    """State for financial advisory workflow."""
    user_profile: dict
    portfolio_analysis: dict
    retirement_plan: dict
    risk_assessment: dict
    final_recommendation: dict


# Financial analysis tools
@tool
def analyze_portfolio(user_profile: dict) -> dict:
    """Analyze and recommend portfolio allocation."""
    allocation = calculate_portfolio_allocation(
        user_profile.get("annual_income", 0),
        user_profile.get("risk_tolerance", "moderate"),
        5
    )
    return {
        "allocation": allocation,
        "assets": generate_asset_recommendations(allocation, user_profile.get("risk_tolerance", "moderate"))
    }


@tool
def analyze_retirement(user_profile: dict) -> dict:
    """Analyze retirement needs and projections."""
    current_age = user_profile.get("age", 30)
    annual_income = user_profile.get("annual_income", 0)
    current_savings = user_profile.get("current_savings", 0)

    retirement_needs = calculate_retirement_needs(
        current_age,
        65,
        annual_income * 0.7
    )

    projection = estimate_retirement_income(
        current_savings,
        annual_income * 0.15,
        65 - current_age
    )

    return {
        "retirement_age": 65,
        "retirement_needs": retirement_needs,
        "projected_balance": projection.get("projected_balance"),
        "annual_income_at_retirement": projection.get("annual_income_4pct_rule"),
        "status": "on_track" if projection.get("projected_balance", 0) >= retirement_needs else "needs_improvement"
    }


@tool
def assess_risk(user_profile: dict) -> dict:
    """Assess financial risk profile."""
    annual_income = user_profile.get("annual_income", 0)
    monthly_debt = user_profile.get("debt", 0) / 12
    current_savings = user_profile.get("current_savings", 0)

    dti = assess_debt_to_income_ratio(annual_income, monthly_debt)
    emergency_fund_target = annual_income / 4

    return {
        "debt_to_income_ratio": dti.get("ratio"),
        "debt_assessment": dti.get("rating"),
        "emergency_fund_target": emergency_fund_target,
        "emergency_fund_status": "adequate" if current_savings >= emergency_fund_target else "needs_improvement",
        "overall_risk_level": determine_risk_level(user_profile, dti.get("ratio"))
    }


def generate_asset_recommendations(allocation: dict, risk_tolerance: str) -> list:
    """Generate specific asset recommendations based on allocation."""
    asset_pools = {
        "conservative": [
            {"symbol": "BND", "name": "Total Bond Market ETF", "sector": "Fixed Income"},
            {"symbol": "VTI", "name": "Total Stock Market ETF", "sector": "Equities"},
            {"symbol": "VEA", "name": "Developed Markets ETF", "sector": "International"}
        ],
        "moderate": [
            {"symbol": "VTI", "name": "Total Stock Market ETF", "sector": "Equities"},
            {"symbol": "VEA", "name": "Developed Markets ETF", "sector": "International"},
            {"symbol": "BND", "name": "Total Bond Market ETF", "sector": "Fixed Income"},
            {"symbol": "VNQ", "name": "Real Estate ETF", "sector": "Real Estate"}
        ],
        "aggressive": [
            {"symbol": "QQQ", "name": "Nasdaq-100 ETF", "sector": "Technology"},
            {"symbol": "VGT", "name": "Information Technology ETF", "sector": "Technology"},
            {"symbol": "VUG", "name": "Growth ETF", "sector": "Growth"},
            {"symbol": "VEA", "name": "Developed Markets ETF", "sector": "International"}
        ]
    }

    assets = asset_pools.get(risk_tolerance, asset_pools["moderate"])
    return [{"symbol": a["symbol"], "name": a["name"], "sector": a["sector"], "allocation": allocation.get(key, 0)}
            for key, a in zip(["stocks", "bonds", "cash"], assets[:3])]


def determine_risk_level(user_profile: dict, dti_ratio: float) -> str:
    """Determine overall financial risk level."""
    risk_factors = 0
    if dti_ratio > 0.25:
        risk_factors += 1
    if user_profile.get("current_savings", 0) < user_profile.get("annual_income", 1) / 4:
        risk_factors += 1
    if user_profile.get("debt", 0) > user_profile.get("annual_income", 1) * 0.5:
        risk_factors += 1

    if risk_factors >= 2:
        return "high"
    elif risk_factors == 1:
        return "moderate"
    return "low"


def portfolio_analysis_node(state: FinancialAdvisoryState) -> FinancialAdvisoryState:
    """Portfolio analysis node."""
    analysis = analyze_portfolio(state["user_profile"])
    state["portfolio_analysis"] = analysis
    return state


def retirement_planning_node(state: FinancialAdvisoryState) -> FinancialAdvisoryState:
    """Retirement planning node."""
    plan = analyze_retirement(state["user_profile"])
    state["retirement_plan"] = plan
    return state


def risk_assessment_node(state: FinancialAdvisoryState) -> FinancialAdvisoryState:
    """Risk assessment node."""
    assessment = assess_risk(state["user_profile"])
    state["risk_assessment"] = assessment
    return state


def recommendation_node(state: FinancialAdvisoryState) -> FinancialAdvisoryState:
    """Generate final recommendations."""
    llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")

    prompt = f"""
    Based on the following financial analysis for a user, provide a comprehensive financial advisory recommendation.

    User Profile:
    {json.dumps(state['user_profile'], indent=2)}

    Portfolio Analysis:
    {json.dumps(state.get('portfolio_analysis', {}), indent=2)}

    Retirement Plan:
    {json.dumps(state.get('retirement_plan', {}), indent=2)}

    Risk Assessment:
    {json.dumps(state.get('risk_assessment', {}), indent=2)}

    Please provide:
    1. Key recommendations
    2. Action items for the next 90 days
    3. Long-term strategy
    4. Risk mitigation steps
    """

    response = llm.invoke(prompt)
    state["final_recommendation"] = {
        "recommendation": response.content,
        "confidence": "high"
    }
    return state


def create_financial_advisor():
    """Create and return the financial advisor workflow graph."""
    workflow = StateGraph(FinancialAdvisoryState)

    # Add nodes
    workflow.add_node("portfolio_analysis", portfolio_analysis_node)
    workflow.add_node("retirement_planning", retirement_planning_node)
    workflow.add_node("risk_assessment", risk_assessment_node)
    workflow.add_node("recommendations", recommendation_node)

    # Add edges
    workflow.add_edge(START, "portfolio_analysis")
    workflow.add_edge(START, "retirement_planning")
    workflow.add_edge(START, "risk_assessment")
    workflow.add_edge("portfolio_analysis", "recommendations")
    workflow.add_edge("retirement_planning", "recommendations")
    workflow.add_edge("risk_assessment", "recommendations")
    workflow.add_edge("recommendations", END)

    return workflow.compile()
