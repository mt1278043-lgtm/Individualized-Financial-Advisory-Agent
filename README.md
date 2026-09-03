# Individualized Financial Advisory Agent

An intelligent financial advisory system powered by LangGraph and Claude that provides personalized investment and financial planning recommendations.

## Features

- **Multi-Agent Architecture**: Portfolio analysis, market research, and risk assessment agents
- **Personalized Recommendations**: Tailored financial advice based on user profile and goals
- **Real-time Analysis**: Market data integration and financial calculations
- **Risk Management**: Comprehensive risk assessment and diversification strategies
- **Compliance**: Built-in guardrails and ethical investment guidelines

## Tech Stack

- **LangGraph**: Agent orchestration and workflow management
- **Claude**: Core AI intelligence for financial analysis
- **Python 3.10+**: Backend runtime
- **LangChain**: LLM framework integration

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Set environment variables:
```bash
export ANTHROPIC_API_KEY="your-api-key"
```

## Project Structure

```
.
├── src/
│   ├── agents/           # Individual agent implementations
│   ├── tools/            # Financial tools and utilities
│   ├── workflows/        # LangGraph workflow definitions
│   ├── models/           # Data models and schemas
│   └── main.py          # Entry point
├── config/              # Configuration files
├── tests/               # Unit and integration tests
└── requirements.txt     # Python dependencies
```

## Usage

### Web Interface (Recommended)
```bash
streamlit run app.py
```
Visit `http://localhost:8501` in your browser

### Python API
```python
from src.workflows.financial_advisor import create_financial_advisor

# Initialize the advisor
advisor = create_financial_advisor()

# Get financial recommendations
result = advisor.invoke({
    "user_profile": {...},
    "financial_goals": [...],
    "risk_tolerance": "moderate"
})
```

## Streamlit Features

- **Dashboard**: Quick financial metrics and summaries
- **Interactive Analysis**: Input your financial profile and get instant recommendations
- **Multi-tab Results**: Portfolio, Retirement, Risk, and Recommendations views
- **Export Data**: Download analysis as JSON
- **Responsive Design**: Works on desktop and mobile

For deployment instructions, see [STREAMLIT_DEPLOYMENT.md](STREAMLIT_DEPLOYMENT.md)

## License

MIT
