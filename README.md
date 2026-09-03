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

## License

MIT
