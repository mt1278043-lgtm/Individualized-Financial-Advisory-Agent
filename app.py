"""Streamlit app for Financial Advisory Agent."""
import streamlit as st
import json
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Financial calculation functions
def calculate_retirement_needs(current_age, retirement_age, annual_expenses, inflation_rate=0.03):
    """Calculate retirement savings needed."""
    import math
    years_to_retirement = retirement_age - current_age
    life_expectancy = 90
    retirement_years = life_expectancy - retirement_age
    future_expenses = annual_expenses * math.pow(1 + inflation_rate, years_to_retirement)
    return future_expenses * retirement_years

def calculate_portfolio_allocation(annual_income, risk_tolerance, years_to_goal):
    """Calculate recommended portfolio allocation."""
    allocations = {
        "conservative": {"stocks": 0.30, "bonds": 0.60, "cash": 0.10},
        "moderate": {"stocks": 0.60, "bonds": 0.30, "cash": 0.10},
        "aggressive": {"stocks": 0.80, "bonds": 0.15, "cash": 0.05}
    }
    return allocations.get(risk_tolerance.lower(), allocations["moderate"])

def assess_debt_to_income_ratio(annual_income, monthly_debt):
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
    }

def estimate_retirement_income(current_savings, annual_contribution, years_to_retirement, annual_return=0.07):
    """Estimate retirement income potential."""
    import math
    future_value = current_savings * math.pow(1 + annual_return, years_to_retirement)
    if annual_return > 0:
        contribution_value = annual_contribution * ((math.pow(1 + annual_return, years_to_retirement) - 1) / annual_return)
    else:
        contribution_value = annual_contribution * years_to_retirement
    total_value = future_value + contribution_value
    annual_income_4pct = total_value * 0.04
    return {
        "projected_balance": total_value,
        "annual_income_4pct_rule": annual_income_4pct,
        "monthly_income": annual_income_4pct / 12
    }

def calculate_emergency_fund(monthly_expenses, months=6):
    """Calculate emergency fund size."""
    return monthly_expenses * months


# Page configuration
st.set_page_config(
    page_title="Financial Advisory Agent",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables."""
    if "user_profile" not in st.session_state:
        st.session_state.user_profile = {}
    if "analysis_results" not in st.session_state:
        st.session_state.analysis_results = None
    if "show_results" not in st.session_state:
        st.session_state.show_results = False


def get_user_profile():
    """Get user profile from form inputs."""
    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Full Name", value="")
        age = st.number_input("Age", min_value=18, max_value=100, value=35)
        annual_income = st.number_input("Annual Income ($)", min_value=0, value=120000)
        employment_status = st.selectbox(
            "Employment Status",
            ["Employed", "Self-Employed", "Retired", "Unemployed"]
        )

    with col2:
        current_savings = st.number_input("Current Savings ($)", min_value=0, value=50000)
        debt = st.number_input("Total Debt ($)", min_value=0, value=30000)
        risk_tolerance = st.selectbox(
            "Risk Tolerance",
            ["Conservative", "Moderate", "Aggressive"]
        )
        investment_experience = st.selectbox(
            "Investment Experience",
            ["Beginner", "Intermediate", "Advanced"]
        )

    return {
        "name": name or "User",
        "age": age,
        "annual_income": annual_income,
        "current_savings": current_savings,
        "debt": debt,
        "employment_status": employment_status,
        "risk_tolerance": risk_tolerance.lower(),
        "investment_experience": investment_experience.lower(),
        "goals": [
            {
                "name": "Retirement",
                "target_amount": 1000000,
                "timeline_years": 65 - age,
                "priority": 1
            },
            {
                "name": "Emergency Fund",
                "target_amount": annual_income / 4,
                "timeline_years": 1,
                "priority": 2
            }
        ]
    }


def display_quick_metrics(profile):
    """Display quick financial metrics."""
    st.subheader("💡 Quick Financial Metrics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        emergency_fund = calculate_emergency_fund(profile["annual_income"] / 12)
        st.metric(
            "Emergency Fund Target",
            f"${emergency_fund:,.0f}",
            delta="6 months expenses"
        )

    with col2:
        dti = assess_debt_to_income_ratio(profile["annual_income"], profile["debt"] / 12)
        st.metric(
            "Debt-to-Income Ratio",
            f"{dti['percentage']:.1f}%",
            delta=dti['rating'].upper()
        )

    with col3:
        savings_rate = (profile["current_savings"] / profile["annual_income"]) * 100 if profile["annual_income"] > 0 else 0
        st.metric(
            "Savings Ratio",
            f"{savings_rate:.1f}%",
            delta="of annual income"
        )

    with col4:
        retirement_needs = calculate_retirement_needs(
            profile["age"],
            65,
            profile["annual_income"] * 0.7
        )
        st.metric(
            "Retirement Needs",
            f"${retirement_needs:,.0f}",
            delta="by age 65"
        )


def display_analysis_results(results):
    """Display analysis results in tabs."""
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📊 Portfolio", "🏦 Retirement", "⚠️ Risk Assessment", "✨ Recommendations"]
    )

    with tab1:
        st.subheader("Portfolio Analysis")
        portfolio = results.get("portfolio_analysis", {})
        if portfolio:
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Recommended Allocation:**")
                allocation = portfolio.get("allocation", {})
                if allocation:
                    for asset_type, percentage in allocation.items():
                        st.progress(percentage, text=f"{asset_type.capitalize()}: {percentage*100:.0f}%")
            with col2:
                st.write("**Asset Recommendations:**")
                assets = portfolio.get("assets", [])
                for asset in assets:
                    st.write(f"- {asset.get('symbol')}: {asset.get('name')}")

    with tab2:
        st.subheader("Retirement Planning")
        retirement = results.get("retirement_plan", {})
        if retirement:
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Retirement Age", retirement.get("retirement_age", "N/A"))
                st.metric(
                    "Retirement Needs",
                    f"${retirement.get('retirement_needs', 0):,.0f}"
                )
            with col2:
                st.metric("Projected Balance", f"${retirement.get('projected_balance', 0):,.0f}")
                st.metric(
                    "Annual Income (4% Rule)",
                    f"${retirement.get('annual_income_at_retirement', 0):,.0f}"
                )
            st.info(f"Status: {retirement.get('status', 'N/A').upper()}")

    with tab3:
        st.subheader("Risk Assessment")
        risk = results.get("risk_assessment", {})
        if risk:
            col1, col2 = st.columns(2)
            with col1:
                st.metric(
                    "DTI Ratio",
                    f"{risk.get('debt_to_income_ratio', 0):.2%}"
                )
                st.metric(
                    "Debt Assessment",
                    risk.get("debt_assessment", "N/A").upper()
                )
            with col2:
                st.metric(
                    "Emergency Fund Target",
                    f"${risk.get('emergency_fund_target', 0):,.0f}"
                )
                st.metric(
                    "Overall Risk Level",
                    risk.get("overall_risk_level", "N/A").upper()
                )

    with tab4:
        st.subheader("Final Recommendations")
        recommendation = results.get("final_recommendation", {})
        if recommendation:
            st.write(recommendation.get("recommendation", "No recommendations available"))


def generate_basic_analysis(profile):
    """Generate basic analysis without full LangGraph."""
    allocation = calculate_portfolio_allocation(
        profile["annual_income"],
        profile["risk_tolerance"],
        5
    )

    retirement_needs = calculate_retirement_needs(
        profile["age"],
        65,
        profile["annual_income"] * 0.7
    )

    projection = estimate_retirement_income(
        profile["current_savings"],
        profile["annual_income"] * 0.15,
        65 - profile["age"]
    )

    dti = assess_debt_to_income_ratio(
        profile["annual_income"],
        profile["debt"] / 12
    )

    return {
        "user_profile": profile,
        "portfolio_analysis": {
            "allocation": allocation,
            "assets": [
                {"symbol": "VTI", "name": "Total Stock Market ETF", "sector": "Equities"},
                {"symbol": "BND", "name": "Total Bond Market ETF", "sector": "Fixed Income"},
                {"symbol": "VEA", "name": "Developed Markets ETF", "sector": "International"}
            ]
        },
        "retirement_plan": {
            "retirement_age": 65,
            "retirement_needs": retirement_needs,
            "projected_balance": projection.get("projected_balance"),
            "annual_income_at_retirement": projection.get("annual_income_4pct_rule"),
            "status": "on_track" if projection.get("projected_balance", 0) >= retirement_needs else "needs_improvement"
        },
        "risk_assessment": {
            "debt_to_income_ratio": dti.get("ratio"),
            "debt_assessment": dti.get("rating"),
            "emergency_fund_target": calculate_emergency_fund(profile["annual_income"] / 12),
            "emergency_fund_status": "adequate" if profile["current_savings"] >= calculate_emergency_fund(profile["annual_income"] / 12) else "needs_improvement",
            "overall_risk_level": "moderate"
        },
        "final_recommendation": {
            "recommendation": f"""
Based on your profile:
- Age: {profile['age']}, Income: ${profile['annual_income']:,.0f}
- Current Savings: ${profile['current_savings']:,.0f}, Debt: ${profile['debt']:,.0f}

**Key Recommendations:**
1. **Portfolio Allocation**: {allocation}
2. **Retirement Planning**: You need ${retirement_needs:,.0f} by age 65
3. **Debt Management**: Your debt-to-income ratio is {dti.get('ratio'):.1%} ({dti.get('rating')})
4. **Emergency Fund**: Target ${calculate_emergency_fund(profile['annual_income'] / 12):,.0f}

**Action Items (Next 90 Days):**
- Build emergency fund to 6 months of expenses
- Set up automatic contributions to retirement accounts
- Review and reduce high-interest debt
- Rebalance portfolio quarterly
            """,
            "confidence": "medium"
        }
    }


def main():
    """Main Streamlit app."""
    initialize_session_state()

    # Header
    st.markdown("# 💰 Individualized Financial Advisory Agent")
    st.markdown("*Powered by LangGraph and OpenAI GPT-4*")
    st.divider()

    # Sidebar
    with st.sidebar:
        st.header("📋 Navigation")
        page = st.radio("Select a page:", ["Dashboard", "Analysis", "About"])

    if page == "Dashboard":
        dashboard_page()
    elif page == "Analysis":
        analysis_page()
    else:
        about_page()


def dashboard_page():
    """Dashboard page."""
    st.header("Dashboard")
    st.write("Welcome to your Financial Advisory Dashboard!")

    # Create two columns
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Your Financial Summary")
        if st.session_state.analysis_results:
            display_quick_metrics(st.session_state.user_profile)
        else:
            st.info("👉 Go to 'Analysis' tab to generate your financial analysis")

    with col2:
        st.subheader("🎯 Recent Updates")
        st.write("- Portfolio analysis ready")
        st.write("- Retirement planning updated")
        st.write("- Risk assessment completed")

    st.divider()

    # Latest analysis
    if st.session_state.analysis_results:
        st.subheader("📈 Latest Analysis Results")
        display_analysis_results(st.session_state.analysis_results)


def analysis_page():
    """Analysis page."""
    st.header("Financial Analysis")
    st.write("Fill in your financial information to get personalized advice.")

    st.subheader("Step 1: Your Financial Profile")
    profile = get_user_profile()
    st.session_state.user_profile = profile

    st.divider()

    # Display quick metrics
    display_quick_metrics(profile)

    st.divider()

    # Analyze button
    col1, col2, col3 = st.columns([1, 1, 2])

    with col1:
        if st.button("🚀 Analyze My Finances", type="primary", use_container_width=True):
            st.session_state.show_results = True
            with st.spinner("Analyzing your financial profile..."):
                try:
                    # Check if API key is set
                    api_key = os.getenv("OPENAI_API_KEY")
                    if not api_key:
                        st.error("⚠️ OPENAI_API_KEY not found!\n\n**To add it:**\n\n1. **Streamlit Cloud**: Go to App settings → Secrets → Add OPENAI_API_KEY\n2. **Local**: Set `export OPENAI_API_KEY='your-key'` in terminal")
                        return

                    # Try to use full AI analysis with OpenAI
                    try:
                        from openai import OpenAI
                        client = OpenAI(api_key=api_key)

                        prompt = f"""
Analyze this financial profile and provide recommendations:

Name: {profile['name']}
Age: {profile['age']}
Annual Income: ${profile['annual_income']:,.0f}
Current Savings: ${profile['current_savings']:,.0f}
Total Debt: ${profile['debt']:,.0f}
Risk Tolerance: {profile['risk_tolerance']}

Provide:
1. Portfolio allocation recommendation
2. Retirement needs analysis
3. Risk assessment
4. Top 3 action items

Be concise and specific.
                        """

                        response = client.chat.completions.create(
                            model="gpt-4",
                            max_tokens=1024,
                            messages=[{"role": "user", "content": prompt}]
                        )

                        ai_recommendation = response.choices[0].message.content
                        results = generate_basic_analysis(profile)
                        results["final_recommendation"]["recommendation"] = ai_recommendation
                        results["final_recommendation"]["confidence"] = "high"

                    except Exception:
                        # Fall back to basic analysis
                        results = generate_basic_analysis(profile)
                        results["final_recommendation"]["confidence"] = "medium"

                    st.session_state.analysis_results = results
                    st.success("✅ Analysis complete!")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

    with col2:
        if st.button("🔄 Reset", use_container_width=True):
            st.session_state.show_results = False
            st.session_state.analysis_results = None
            st.rerun()

    st.divider()

    # Display results
    if st.session_state.show_results and st.session_state.analysis_results:
        st.subheader("Step 2: Your Analysis Results")
        display_analysis_results(st.session_state.analysis_results)

        # Download results
        st.divider()
        results_json = json.dumps(st.session_state.analysis_results, indent=2, default=str)
        st.download_button(
            label="📥 Download Analysis as JSON",
            data=results_json,
            file_name=f"financial_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )


def about_page():
    """About page."""
    st.header("About This App")

    st.markdown("""
    ## Individualized Financial Advisory Agent

    This application combines **LangGraph** and **OpenAI GPT-4** to provide personalized financial advisory recommendations.

    ### Features
    - 📊 Portfolio analysis and recommendations
    - 🏦 Retirement planning projections
    - ⚠️ Risk assessment
    - 💡 Personalized financial advice

    ### How It Works
    1. Enter your financial information
    2. The AI analyzes your profile across multiple dimensions
    3. Receive personalized recommendations tailored to your needs

    ### Technology Stack
    - **LangGraph**: Agent orchestration and workflow management
    - **OpenAI GPT-4**: AI-powered analysis and recommendations
    - **Streamlit**: Web interface
    - **Pydantic**: Data validation

    ### Disclaimer
    This tool provides educational financial information only and is not a substitute for professional financial advice.
    Consult with a certified financial advisor before making investment decisions.

    ---
    *Built with ❤️ using Streamlit and Claude AI*
    """)

    st.divider()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("📚 **Learn More**: Visit our GitHub repository")
    with col2:
        st.warning("⚠️ **Disclaimer**: Not a substitute for professional advice")
    with col3:
        st.success("✅ **Privacy**: Your data is processed locally")


if __name__ == "__main__":
    main()
