import unittest
from datetime import datetime

from portfolio_manager.portfolio import InvestmentPortfolio
from portfolio_manager.return_calculators import TimeWeightedReturnCalculator


class ReturnCalculatorsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.test_portfolio = InvestmentPortfolio(name="test_portfolio")

    def test_time_weighted_return(self):
        # Test that a single sub-period reduces to the simple rate of return
        test_data = [
            {
                'date': datetime(2021, 1, 1),
                'total_deposited': 100,
                'current_portfolio_value': 100,
                'transaction_type': ''
            },
            {
                'date': datetime(2021, 1, 2),
                'total_deposited': 100,
                'current_portfolio_value': 110,
                'transaction_type': ''
            }
        ]
        self.test_portfolio.portfolio_history = test_data
        twr_calculator = TimeWeightedReturnCalculator()
        actual_output = twr_calculator.calculate_return(self.test_portfolio,
                                                        annualised=False)
        expected_output = 10
        self.assertEqual(actual_output, expected_output)

        # Test a multi-period with deposits only
        test_data = [
            {
                'date': datetime(2021, 1, 1),
                'total_deposited': 100,
                'current_portfolio_value': 100,
                'transaction_type': ''
            },
            {
                'date': datetime(2021, 1, 2),
                'total_deposited': 100,
                'current_portfolio_value': 110,
                'transaction_type': ''
            },
            {
                'date': datetime(2021, 1, 3),
                'total_deposited': 200,
                'current_portfolio_value': 210,
                'transaction_type': ''
            },
            {
                'date': datetime(2021, 1, 4),
                'total_deposited': 200,
                'current_portfolio_value': 215,
                'transaction_type': ''
            },
            {
                'date': datetime(2021, 1, 5),
                'total_deposited': 250,
                'current_portfolio_value': 265,
                'transaction_type': ''
            },
            {
                'date': datetime(2021, 1, 6),
                'total_deposited': 250,
                'current_portfolio_value': 280,
                'transaction_type': ''
            }
        ]
        self.test_portfolio.portfolio_history = test_data
        twr_calculator = TimeWeightedReturnCalculator()
        actual_output = twr_calculator.calculate_return(self.test_portfolio,
                                                        annualised=False)
        expected_output = 18.99
        self.assertEqual(actual_output, expected_output)

        # Test a multi-period including deposits and withdrawals
        test_data = [
            {
                'date': datetime(2021, 1, 1),
                'total_deposited': 100,
                'current_portfolio_value': 100,
                'transaction_type': ''
            },
            {
                'date': datetime(2021, 1, 2),
                'total_deposited': 100,
                'current_portfolio_value': 110,
                'transaction_type': ''
            },
            {
                'date': datetime(2021, 1, 3),
                'total_deposited': 50,
                'current_portfolio_value': 60,
                'transaction_type': ''
            },
            {
                'date': datetime(2021, 1, 4),
                'total_deposited': 50,
                'current_portfolio_value': 54,
                'transaction_type': ''
            },
            {
                'date': datetime(2021, 1, 5),
                'total_deposited': 100,
                'current_portfolio_value': 104,
                'transaction_type': ''
            },
            {
                'date': datetime(2021, 1, 6),
                'total_deposited': 100,
                'current_portfolio_value': 119.6,
                'transaction_type': ''
            }
        ]
        self.test_portfolio.portfolio_history = test_data
        twr_calculator = TimeWeightedReturnCalculator()
        actual_output = twr_calculator.calculate_return(self.test_portfolio,
                                                        annualised=False)
        expected_output = 13.85
        self.assertEqual(actual_output, expected_output)


if __name__ == '__main__':
    unittest.main()
