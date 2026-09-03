"""Financial data models and schemas."""
from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum


class RiskTolerance(str, Enum):
    """Risk tolerance levels."""
    CONSERVATIVE = "conservative"
    MODERATE = "moderate"
    AGGRESSIVE = "aggressive"


class FinancialGoal(BaseModel):
    """Individual financial goal."""
    name: str
    target_amount: float
    timeline_years: int
    priority: int = Field(1, ge=1, le=5)


class UserProfile(BaseModel):
    """User financial profile."""
    name: str
    age: int
    annual_income: float
    current_savings: float
    debt: float = 0.0
    employment_status: str
    risk_tolerance: RiskTolerance
    investment_experience: str = "beginner"
    goals: List[FinancialGoal]


class PortfolioAsset(BaseModel):
    """Portfolio asset."""
    symbol: str
    name: str
    allocation_percentage: float
    sector: str


class PortfolioRecommendation(BaseModel):
    """Portfolio recommendation."""
    rationale: str
    recommended_assets: List[PortfolioAsset]
    expected_return: float
    risk_level: str
    rebalance_frequency: str


class FinancialAnalysis(BaseModel):
    """Financial analysis result."""
    user_profile: UserProfile
    portfolio_recommendation: PortfolioRecommendation
    risk_assessment: str
    tax_strategy: str
    retirement_plan: str
    next_steps: List[str]
