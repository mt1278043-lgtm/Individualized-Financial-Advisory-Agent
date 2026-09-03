"""Financial analysis tools and utilities."""
import math
from typing import Dict, Any


def calculate_retirement_needs(
    current_age: int,
    retirement_age: int,
    annual_expenses: float,
    inflation_rate: float = 0.03
) -> float:
    """Calculate retirement savings needed."""
    years_to_retirement = retirement_age - current_age
    life_expectancy = 90
    retirement_years = life_expectancy - retirement_age

    future_expenses = annual_expenses * math.pow(1 + inflation_rate, years_to_retirement)
    total_needed = future_expenses * retirement_years

    return total_needed


def calculate_portfolio_allocation(
    annual_income: float,
    risk_tolerance: str,
    years_to_goal: int
) -> Dict[str, float]:
    """Calculate recommended portfolio allocation."""
    allocations = {
        "conservative": {"stocks": 0.30, "bonds": 0.60, "cash": 0.10},
        "moderate": {"stocks": 0.60, "bonds": 0.30, "cash": 0.10},
        "aggressive": {"stocks": 0.80, "bonds": 0.15, "cash": 0.05}
    }

    return allocations.get(risk_tolerance.lower(), allocations["moderate"])


def calculate_emergency_fund(monthly_expenses: float, months: int = 6) -> float:
    """Calculate recommended emergency fund size."""
    return monthly_expenses * months


def assess_debt_to_income_ratio(annual_income: float, monthly_debt: float) -> Dict[str, Any]:
    """Assess debt-to-income ratio."""
    monthly_income = annual_income / 12
    dti_ratio = monthly_debt / monthly_income if monthly_income > 0 else 0

    if dti_ratio <= 0.15:
        rating = "excellent"
    elif dti_ratio <= 0.25:
        rating = "good"
    elif dti_ratio <= 0.35:
        rating = "acceptable"
    else:
        rating = "concerning"

    return {
        "ratio": dti_ratio,
        "percentage": dti_ratio * 100,
        "rating": rating,
        "recommendation": "Focus on debt reduction" if dti_ratio > 0.25 else "Maintain current strategy"
    }


def calculate_savings_rate(annual_income: float, annual_savings: float) -> Dict[str, float]:
    """Calculate savings rate and efficiency."""
    rate = (annual_savings / annual_income * 100) if annual_income > 0 else 0

    return {
        "savings_rate": rate,
        "rating": "excellent" if rate >= 20 else "good" if rate >= 10 else "needs improvement"
    }


def estimate_retirement_income(
    current_savings: float,
    annual_contribution: float,
    years_to_retirement: int,
    annual_return: float = 0.07
) -> Dict[str, float]:
    """Estimate retirement income potential."""
    future_value = current_savings * math.pow(1 + annual_return, years_to_retirement)

    # Add contributions
    if annual_return > 0:
        contribution_value = annual_contribution * (
            (math.pow(1 + annual_return, years_to_retirement) - 1) / annual_return
        )
    else:
        contribution_value = annual_contribution * years_to_retirement

    total_value = future_value + contribution_value
    annual_income_4pct = total_value * 0.04

    return {
        "projected_balance": total_value,
        "annual_income_4pct_rule": annual_income_4pct,
        "monthly_income": annual_income_4pct / 12
    }
