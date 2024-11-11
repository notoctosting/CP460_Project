import unittest
from scripts.financial_metrics import calculate_var, calculate_sharpe_ratio

class TestFinancialMetrics(unittest.TestCase):
    def test_calculate_var(self):
        returns = [0.05, 0.04, -0.01]
        var = calculate_var(returns)
        self.assertEqual(var, -0.01)

    def test_calculate_sharpe_ratio(self):
        returns = [0.05, 0.04, -0.01]
        sharpe = calculate_sharpe_ratio(returns)
        self.assertAlmostEqual(sharpe, 0.45, places=2)

if __name__ == "__main__":
    unittest.main()
