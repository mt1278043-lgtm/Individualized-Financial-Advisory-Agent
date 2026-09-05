"""Main entry point for the Financial Advisory Agent."""
import os
import json
from dotenv import load_dotenv
from src.workflows.financial_advisor import create_financial_advisor
from src.models.financial import UserProfile, RiskTolerance, FinancialGoal


def load_environment():
    """Load environment variables."""
    load_dotenv()
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY environment variable not set")


def example_user_profile() -> dict:
    """Create an example user profile for testing."""
    return {
        "name": "John Doe",
        "age": 35,
        "annual_income": 120000,
        "current_savings": 50000,
        "debt": 30000,
        "employment_status": "employed",
        "risk_tolerance": "moderate",
        "investment_experience": "intermediate",
        "goals": [
            {
                "name": "Retirement",
                "target_amount": 1000000,
                "timeline_years": 30,
                "priority": 1
            },
            {
                "name": "House Down Payment",
                "target_amount": 100000,
                "timeline_years": 5,
                "priority": 2
            }
        ]
    }


def main():
    """Main function to run the financial advisor."""
    load_environment()

    print("=" * 60)
    print("Individualized Financial Advisory Agent")
    print("=" * 60)
    print()

    # Create the advisor workflow
    advisor = create_financial_advisor()

    # Example user profile
    user_profile = example_user_profile()
    print(f"Analyzing financial profile for: {user_profile['name']}")
    print()

    # Run the advisor
    state = {
        "user_profile": user_profile,
        "portfolio_analysis": {},
        "retirement_plan": {},
        "risk_assessment": {},
        "final_recommendation": {}
    }

    result = advisor.invoke(state)

    # Display results
    print("PORTFOLIO ANALYSIS")
    print("-" * 60)
    print(json.dumps(result.get("portfolio_analysis", {}), indent=2))
    print()

    print("RETIREMENT PLAN")
    print("-" * 60)
    print(json.dumps(result.get("retirement_plan", {}), indent=2))
    print()

    print("RISK ASSESSMENT")
    print("-" * 60)
    print(json.dumps(result.get("risk_assessment", {}), indent=2))
    print()

    print("RECOMMENDATIONS")
    print("-" * 60)
    recommendation = result.get("final_recommendation", {})
    print(recommendation.get("recommendation", "No recommendations available"))
    print()


if __name__ == "__main__":
    main()
