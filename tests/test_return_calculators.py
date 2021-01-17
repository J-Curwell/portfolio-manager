import unittest
from datetime import datetime
from unittest.mock import MagicMock

from portfolio_manager.portfolio import InvestmentPortfolio
from portfolio_manager.return_calculators import (TimeWeightedReturnCalculator,
                                                  ReturnCalculator)


class ReturnCalculatorsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.test_portfolio = InvestmentPortfolio(name="test_portfolio")

    def test_calculate_annualised_return(self):
        # Test a portfolio age of < 1
        mock_rc = MagicMock()
        mock_rc.get_portfolio_age.return_value = 0.9
        actual = ReturnCalculator.calculate_annualised_return(mock_rc, 'test', 13)
        mock_rc.get_portfolio_age.assert_called_once_with('test')
        expected = 14.54
        self.assertEqual(expected, actual)

        # Test a portfolio age of 1
        mock_rc = MagicMock()
        mock_rc.get_portfolio_age.return_value = 1
        actual = ReturnCalculator.calculate_annualised_return(mock_rc, 'test', -11)
        mock_rc.get_portfolio_age.assert_called_once_with('test')
        expected = -11
        self.assertEqual(expected, actual)

        # Test a portfolio age of > 1
        mock_rc = MagicMock()
        mock_rc.get_portfolio_age.return_value = 2.5
        actual = ReturnCalculator.calculate_annualised_return(mock_rc, 'test', 120)
        mock_rc.get_portfolio_age.assert_called_once_with('test')
        expected = 37.08
        self.assertEqual(expected, actual)

    def test_get_portfolio_age_shorter(self):
        # Test a portfolio of age < 1 year
        test_data = [
            {
                'date': datetime(2020, 7, 1)
            },
            {
                'date': datetime(2021, 1, 1),
            }
        ]
        self.test_portfolio.portfolio_history = test_data
        actual_years = ReturnCalculator.get_portfolio_age(self.test_portfolio)
        self.assertEqual(0.5, actual_years)
        actual_months = ReturnCalculator.get_portfolio_age(self.test_portfolio, 'months')
        self.assertEqual(6, actual_months)
        actual_days = ReturnCalculator.get_portfolio_age(self.test_portfolio, 'days')
        self.assertEqual(184, actual_days)

    def test_get_portfolio_age_medium(self):
        # Test a portfolio of age 1 year
        test_data = [
            {
                'date': datetime(2020, 7, 1)
            },
            {
                'date': datetime(2021, 1, 1),
            },
            {
                'date': datetime(2021, 7, 1)
            }
        ]
        self.test_portfolio.portfolio_history = test_data
        actual_years = ReturnCalculator.get_portfolio_age(self.test_portfolio, 'years')
        self.assertEqual(1, actual_years)
        actual_months = ReturnCalculator.get_portfolio_age(self.test_portfolio, 'months')
        self.assertEqual(12, actual_months)
        actual_days = ReturnCalculator.get_portfolio_age(self.test_portfolio, 'days')
        self.assertEqual(365, actual_days)

    def test_get_portfolio_age_longer(self):
        # Test a portfolio of age > 1 year
        test_data = [
            {
                'date': datetime(2020, 7, 1)
            },
            {
                'date': datetime(2021, 1, 1),
            },
            {
                'date': datetime(2021, 1, 1),
            },
            {
                'date': datetime(2022, 9, 1)
            }
        ]
        self.test_portfolio.portfolio_history = test_data
        actual_years = ReturnCalculator.get_portfolio_age(self.test_portfolio)
        self.assertEqual(2.17, actual_years)
        actual_months = ReturnCalculator.get_portfolio_age(self.test_portfolio, 'months')
        self.assertEqual(26, actual_months)
        actual_days = ReturnCalculator.get_portfolio_age(self.test_portfolio, 'days')
        self.assertEqual(792, actual_days)


class SimpleReturnCalculatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.test_portfolio = InvestmentPortfolio(name="test_portfolio")


class TimeWeightedReturnCalculatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.test_portfolio = InvestmentPortfolio(name="test_portfolio")

    def test_time_weighted_return_single_period(self):
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

    def test_time_weighted_return_multi_deposits(self):
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

    def test_time_weighted_return_mixed_periods(self):
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

    def test_time_weighted_return_negative_return(self):
        # Test a multi-period including deposits and negative return
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
                'current_portfolio_value': 80,
                'transaction_type': ''
            },
            {
                'date': datetime(2021, 1, 3),
                'total_deposited': 50,
                'current_portfolio_value': 30,
                'transaction_type': ''
            },
            {
                'date': datetime(2021, 1, 4),
                'total_deposited': 50,
                'current_portfolio_value': 27,
                'transaction_type': ''
            },
            {
                'date': datetime(2021, 1, 5),
                'total_deposited': 100,
                'current_portfolio_value': 77,
                'transaction_type': ''
            },
            {
                'date': datetime(2021, 1, 6),
                'total_deposited': 100,
                'current_portfolio_value': 78.54,
                'transaction_type': ''
            }
        ]
        self.test_portfolio.portfolio_history = test_data
        twr_calculator = TimeWeightedReturnCalculator()
        actual_output = twr_calculator.calculate_return(self.test_portfolio,
                                                        annualised=False)
        expected_output = -26.56
        self.assertEqual(actual_output, expected_output)


if __name__ == '__main__':
    unittest.main()
