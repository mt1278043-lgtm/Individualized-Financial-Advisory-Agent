"""Tests for financial tools."""
import unittest
from src.tools.financial_tools import (
    calculate_retirement_needs,
    calculate_portfolio_allocation,
    calculate_emergency_fund,
    assess_debt_to_income_ratio,
    calculate_savings_rate,
    estimate_retirement_income
)


class TestFinancialTools(unittest.TestCase):
    """Test financial calculation tools."""

    def test_calculate_retirement_needs(self):
        """Test retirement needs calculation."""
        result = calculate_retirement_needs(35, 65, 60000)
        self.assertIsInstance(result, float)
        self.assertGreater(result, 0)

    def test_calculate_portfolio_allocation(self):
        """Test portfolio allocation calculation."""
        result = calculate_portfolio_allocation(100000, "moderate", 5)
        self.assertIsInstance(result, dict)
        self.assertIn("stocks", result)
        self.assertIn("bonds", result)
        self.assertIn("cash", result)

    def test_calculate_emergency_fund(self):
        """Test emergency fund calculation."""
        result = calculate_emergency_fund(5000)
        self.assertEqual(result, 30000)

    def test_assess_debt_to_income_ratio(self):
        """Test debt-to-income ratio assessment."""
        result = assess_debt_to_income_ratio(120000, 1000)
        self.assertIsInstance(result, dict)
        self.assertIn("ratio", result)
        self.assertIn("rating", result)

    def test_calculate_savings_rate(self):
        """Test savings rate calculation."""
        result = calculate_savings_rate(100000, 20000)
        self.assertEqual(result["savings_rate"], 20.0)

    def test_estimate_retirement_income(self):
        """Test retirement income estimation."""
        result = estimate_retirement_income(100000, 10000, 30)
        self.assertIn("projected_balance", result)
        self.assertIn("annual_income_4pct_rule", result)


if __name__ == "__main__":
    unittest.main()
