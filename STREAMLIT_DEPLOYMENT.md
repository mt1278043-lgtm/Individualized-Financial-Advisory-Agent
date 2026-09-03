# Streamlit Deployment Guide

This guide covers how to run and deploy the Financial Advisory Agent with Streamlit.

## Local Development

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables
Create a `.env` file in the project root:
```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
export ANTHROPIC_API_KEY="your-api-key-here"
```

### 3. Run Streamlit App Locally
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Features

- **Dashboard**: View your financial summary and quick metrics
- **Analysis**: Input your financial information and get AI-powered analysis
- **Results**: View portfolio recommendations, retirement planning, and risk assessment
- **Download**: Export your analysis as JSON

## Streamlit Cloud Deployment

### 1. Push to GitHub
Ensure your repository is pushed to GitHub:
```bash
git push origin claude/push-github-langgraph-u7lzd9
```

### 2. Deploy to Streamlit Cloud
1. Go to [https://streamlit.io/cloud](https://streamlit.io/cloud)
2. Click "New app"
3. Select your GitHub repository
4. Choose the branch: `claude/push-github-langgraph-u7lzd9`
5. Set main file path: `streamlit_app.py`
6. Click "Deploy"

### 3. Add Secrets
In Streamlit Cloud dashboard:
1. Go to App Settings → Secrets
2. Add your ANTHROPIC_API_KEY:
```toml
ANTHROPIC_API_KEY = "your-api-key-here"
```

## Docker Deployment (Optional)

Create a `Dockerfile`:
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["streamlit", "run", "app.py"]
```

Build and run:
```bash
docker build -t financial-advisor .
docker run -p 8501:8501 -e ANTHROPIC_API_KEY="your-key" financial-advisor
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `ANTHROPIC_API_KEY` | Anthropic API key | Yes |
| `CLAUDE_MODEL` | Claude model to use (default: claude-3-5-sonnet-20241022) | No |
| `LOG_LEVEL` | Logging level (default: INFO) | No |

## Troubleshooting

### Import Error: No module named 'src'
Make sure you're running from the project root directory.

### API Key not found
Ensure `ANTHROPIC_API_KEY` is set in your environment or `.env` file.

### Streamlit not responding
Try clearing cache:
```bash
streamlit cache clear
```

## Performance Notes

- First run may take 30-60 seconds as Claude analyzes your profile
- Subsequent runs use caching for faster results
- Analysis runs in parallel using LangGraph

## Support

For issues or questions:
1. Check Streamlit docs: https://docs.streamlit.io
2. Check Anthropic docs: https://docs.anthropic.com
3. Open an issue on GitHub

---

**Last Updated**: 2026-09-03
