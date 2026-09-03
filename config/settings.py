"""Application settings and configuration."""
import os
from typing import Optional


class Settings:
    """Application settings."""

    # API Configuration
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    CLAUDE_MODEL: str = os.getenv("CLAUDE_MODEL", "claude-3-5-sonnet-20241022")

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # Financial Parameters
    DEFAULT_RETIREMENT_AGE: int = 65
    DEFAULT_INFLATION_RATE: float = 0.03
    DEFAULT_ANNUAL_RETURN: float = 0.07
    EMERGENCY_FUND_MONTHS: int = 6

    # Portfolio Configuration
    PORTFOLIO_REBALANCE_FREQUENCY: str = "quarterly"
    MIN_ASSET_ALLOCATION: float = 0.05
    MAX_ASSET_ALLOCATION: float = 0.95

    @classmethod
    def validate(cls) -> bool:
        """Validate required settings."""
        if not cls.ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY is required")
        return True


# Global settings instance
settings = Settings()
