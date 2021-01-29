import unittest
from datetime import datetime
from unittest.mock import MagicMock

from numpy_financial import irr
from portfolio_manager.exceptions import InsufficientData
from portfolio_manager.portfolio import InvestmentPortfolio
from portfolio_manager.return_calculators import (TimeWeightedReturnCalculator,
                                                  ReturnCalculator,
                                                  SimpleReturnCalculator,
                                                  MoneyWeightedReturnCalculator)


class ReturnCalculatorsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.test_portfolio = InvestmentPortfolio(name="test_portfolio")

    def test_calculate_annualised_return(self):
        # Test a portfolio age of < 1
        mock_rc = MagicMock()
        mock_rc._get_portfolio_age.return_value = 0.9
        actual = ReturnCalculator.calculate_annualised_return(mock_rc, 'test', 13)
        mock_rc._get_portfolio_age.assert_called_once_with('test')
        expected = 14.54
        self.assertEqual(expected, actual)

        # Test a portfolio age of 1
        mock_rc = MagicMock()
        mock_rc._get_portfolio_age.return_value = 1
        actual = ReturnCalculator.calculate_annualised_return(mock_rc, 'test', -11)
        mock_rc._get_portfolio_age.assert_called_once_with('test')
        expected = -11
        self.assertEqual(expected, actual)

        # Test a portfolio age of > 1
        mock_rc = MagicMock()
        mock_rc._get_portfolio_age.return_value = 2.5
        actual = ReturnCalculator.calculate_annualised_return(mock_rc, 'test', 120)
        mock_rc._get_portfolio_age.assert_called_once_with('test')
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
        actual = ReturnCalculator._get_portfolio_age(self.test_portfolio)
        self.assertEqual(0.5, round(actual, 2))

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
        actual = ReturnCalculator._get_portfolio_age(self.test_portfolio)
        self.assertEqual(1, round(actual, 2))

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
        actual = ReturnCalculator._get_portfolio_age(self.test_portfolio)
        self.assertEqual(2.17, round(actual, 2))


class SimpleReturnCalculatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.test_portfolio = InvestmentPortfolio(name="test_portfolio")
        self.simple_return_calculator = SimpleReturnCalculator()

    def test_calculate_return_no_portfolio_data(self):
        # Test that one or less transaction results in an error
        with self.assertRaises(InsufficientData):
            self.simple_return_calculator.calculate_return(self.test_portfolio,
                                                           annualised=False)

    def test_calculate_return_negative_deposited(self):
        # This is an example of how a real portfolio could have a negative total
        # deposited value
        test_data = [
            {
                # Deposit £100
                'date': datetime(2021, 1, 1),
                'total_deposited': 100,
                'current_portfolio_value': 100,
                'transaction_type': 'deposit'
            },
            {
                # Value increases to £110
                'date': datetime(2021, 1, 2),
                'total_deposited': 100,
                'current_portfolio_value': 110,
                'transaction_type': 'update_portfolio_value'
            },
            {
                # Withdraw £105, leaving £5 in the portfolio with total deposited = -£5
                'date': datetime(2021, 1, 2),
                'total_deposited': -5,
                'current_portfolio_value': 5,
                'transaction_type': 'update_portfolio_value'
            }
        ]
        # Test that negative total deposited raises an error
        self.test_portfolio.portfolio_history = test_data
        self.test_portfolio.total_deposited = -5
        with self.assertRaises(ValueError):
            self.simple_return_calculator.calculate_return(self.test_portfolio,
                                                           annualised=False)

    def test_calculate_return_zero_deposited(self):
        # This is an example of how a real portfolio could have a total deposited value
        # of zero
        test_data = [
            {
                # Deposit £100
                'date': datetime(2021, 1, 1),
                'total_deposited': 100,
                'current_portfolio_value': 100,
                'transaction_type': 'deposit'
            },
            {
                # Value increases to £110
                'date': datetime(2021, 1, 2),
                'total_deposited': 100,
                'current_portfolio_value': 110,
                'transaction_type': 'update_portfolio_value'
            },
            {
                # Withdraw £100, leaving £10 in the portfolio with total deposited = £0
                'date': datetime(2021, 1, 2),
                'total_deposited': -5,
                'current_portfolio_value': 5,
                'transaction_type': 'update_portfolio_value'
            }
        ]
        # Test that zero total deposited raises an error
        self.test_portfolio.portfolio_history = test_data
        self.test_portfolio.total_deposited = 0
        with self.assertRaises(ValueError):
            self.simple_return_calculator.calculate_return(self.test_portfolio,
                                                           annualised=False)

    def test_calculate_return_positive_return(self):
        # Ensure the portfolio has non-empty history to prevent an error
        test_data = ["I'm", "not", "empty"]
        self.test_portfolio.portfolio_history = test_data

        # Test 10% return
        self.test_portfolio.total_deposited = 100
        self.test_portfolio.current_portfolio_value = 110
        actual = self.simple_return_calculator.calculate_return(self.test_portfolio,
                                                                annualised=False)
        self.assertEqual(10, actual)

        # Test 110% return
        self.test_portfolio.total_deposited = 40
        self.test_portfolio.current_portfolio_value = 84
        actual = self.simple_return_calculator.calculate_return(self.test_portfolio,
                                                                annualised=False)
        self.assertEqual(110, actual)

    def test_calculate_return_negative_return(self):
        # Ensure the portfolio has non-empty history to prevent an error
        test_data = ["I'm", "not", "empty"]
        self.test_portfolio.portfolio_history = test_data

        # Test -10% return
        self.test_portfolio.total_deposited = 100
        self.test_portfolio.current_portfolio_value = 90
        actual = self.simple_return_calculator.calculate_return(self.test_portfolio,
                                                                annualised=False)
        self.assertEqual(-10, actual)

        # Test -35% return
        self.test_portfolio.total_deposited = 40
        self.test_portfolio.current_portfolio_value = 26
        actual = self.simple_return_calculator.calculate_return(self.test_portfolio,
                                                                annualised=False)
        self.assertEqual(-35, actual)

        # Test -100% return
        self.test_portfolio.total_deposited = 40
        self.test_portfolio.current_portfolio_value = 0
        actual = self.simple_return_calculator.calculate_return(self.test_portfolio,
                                                                annualised=False)
        self.assertEqual(-100, actual)


class TimeWeightedReturnCalculatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.test_portfolio = InvestmentPortfolio(name="test_portfolio")
        self.twr_calculator = TimeWeightedReturnCalculator()

    def test_calculate_return_no_data(self):
        # Test that one or less transaction results in an error
        with self.assertRaises(InsufficientData):
            self.twr_calculator.calculate_return(self.test_portfolio, annualised=False)

    def test_calculate_return_single_period(self):
        # Test that a single sub-period reduces to the simple rate of return
        test_data = [
            {
                'date': datetime(2021, 1, 1),
                'total_deposited': 100,
                'current_portfolio_value': 100,
                'transaction_type': 'deposit'
            },
            {
                'date': datetime(2021, 1, 2),
                'total_deposited': 100,
                'current_portfolio_value': 110,
                'transaction_type': 'update_portfolio_value'
            }
        ]
        self.test_portfolio.portfolio_history = test_data
        actual_output = self.twr_calculator.calculate_return(self.test_portfolio,
                                                             annualised=False)
        expected_output = 10
        self.assertEqual(actual_output, expected_output)

    def test_calculate_return_multi_deposits(self):
        # Test a multi-period with deposits only
        test_data = [
            {
                'date': datetime(2021, 1, 1),
                'total_deposited': 100,
                'current_portfolio_value': 100,
                'transaction_type': 'deposit'
            },
            {
                'date': datetime(2021, 1, 2),
                'total_deposited': 100,
                'current_portfolio_value': 110,
                'transaction_type': 'update_portfolio_value'
            },
            {
                'date': datetime(2021, 1, 3),
                'total_deposited': 200,
                'current_portfolio_value': 210,
                'transaction_type': 'deposit'
            },
            {
                'date': datetime(2021, 1, 4),
                'total_deposited': 200,
                'current_portfolio_value': 215,
                'transaction_type': 'update_portfolio_value'
            },
            {
                'date': datetime(2021, 1, 5),
                'total_deposited': 250,
                'current_portfolio_value': 265,
                'transaction_type': 'deposit'
            },
            {
                'date': datetime(2021, 1, 6),
                'total_deposited': 250,
                'current_portfolio_value': 280,
                'transaction_type': 'update_portfolio_value'
            }
        ]
        self.test_portfolio.portfolio_history = test_data
        actual_output = self.twr_calculator.calculate_return(self.test_portfolio,
                                                             annualised=False)
        expected_output = 18.99
        self.assertEqual(actual_output, expected_output)

    def test_calculate_return_mixed_periods(self):
        # Test a multi-period including deposits and withdrawals
        test_data = [
            {
                'date': datetime(2021, 1, 1),
                'total_deposited': 100,
                'current_portfolio_value': 100,
                'transaction_type': 'deposit'
            },
            {
                'date': datetime(2021, 1, 2),
                'total_deposited': 100,
                'current_portfolio_value': 110,
                'transaction_type': 'update_portfolio_value'
            },
            {
                'date': datetime(2021, 1, 3),
                'total_deposited': 50,
                'current_portfolio_value': 60,
                'transaction_type': 'withdrawal'
            },
            {
                'date': datetime(2021, 1, 4),
                'total_deposited': 50,
                'current_portfolio_value': 54,
                'transaction_type': 'update_portfolio_value'
            },
            {
                'date': datetime(2021, 1, 5),
                'total_deposited': 100,
                'current_portfolio_value': 104,
                'transaction_type': 'deposit'
            },
            {
                'date': datetime(2021, 1, 6),
                'total_deposited': 100,
                'current_portfolio_value': 119.6,
                'transaction_type': 'update_portfolio_value'
            }
        ]
        self.test_portfolio.portfolio_history = test_data
        actual_output = self.twr_calculator.calculate_return(self.test_portfolio,
                                                             annualised=False)
        expected_output = 13.85
        self.assertEqual(actual_output, expected_output)

    def test_calculate_return_negative_return(self):
        # Test a multi-period including deposits and negative return
        test_data = [
            {
                'date': datetime(2021, 1, 1),
                'total_deposited': 100,
                'current_portfolio_value': 100,
                'transaction_type': 'deposit'
            },
            {
                'date': datetime(2021, 1, 2),
                'total_deposited': 100,
                'current_portfolio_value': 80,
                'transaction_type': 'update_portfolio_value'
            },
            {
                'date': datetime(2021, 1, 3),
                'total_deposited': 50,
                'current_portfolio_value': 30,
                'transaction_type': 'withdrawal'
            },
            {
                'date': datetime(2021, 1, 4),
                'total_deposited': 50,
                'current_portfolio_value': 27,
                'transaction_type': 'update_portfolio_value'
            },
            {
                'date': datetime(2021, 1, 5),
                'total_deposited': 100,
                'current_portfolio_value': 77,
                'transaction_type': 'deposit'
            },
            {
                'date': datetime(2021, 1, 6),
                'total_deposited': 100,
                'current_portfolio_value': 78.54,
                'transaction_type': 'update_portfolio_value'
            }
        ]
        self.test_portfolio.portfolio_history = test_data
        actual_output = self.twr_calculator.calculate_return(self.test_portfolio,
                                                             annualised=False)
        expected_output = -26.56
        self.assertEqual(actual_output, expected_output)


class MoneyWeightedReturnCalculatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.test_portfolio = InvestmentPortfolio(name="test_portfolio")
        self.mwr_calculator = MoneyWeightedReturnCalculator()

    def test_calculate_return_no_data(self):
        # Test that one or less transaction results in an error
        with self.assertRaises(ValueError):
            self.mwr_calculator.calculate_return(self.test_portfolio, annualised=False)

    def test_calculate_return_single_period(self):
        # Test that a single sub-period reduces to the simple rate of return
        test_data = [
            {
                'date': datetime(2021, 1, 1),
                'total_deposited': 100,
                'current_portfolio_value': 100,
                'transaction_type': 'deposit'
            },
            {
                'date': datetime(2021, 1, 2),
                'total_deposited': 100,
                'current_portfolio_value': 110,
                'transaction_type': 'update_portfolio_value'
            }
        ]
        self.test_portfolio.portfolio_history = test_data
        actual_output = self.mwr_calculator.calculate_return(self.test_portfolio,
                                                             annualised=False)
        expected_output = 10
        self.assertEqual(actual_output, expected_output)

    def test_calculate_return_deposits_and_withdrawals(self):
        # Test a multi-period with deposits and withdrawals
        test_data = [
            {
                'date': datetime(2019, 1, 1),
                'total_deposited': 50,
                'current_portfolio_value': 50,
                'transaction_type': 'deposit'
            },
            {
                'date': datetime(2020, 1, 1),
                'total_deposited': 50,
                'current_portfolio_value': 52,
                'transaction_type': 'update_portfolio_value'
            },

            {
                'date': datetime(2020, 1, 1),
                'total_deposited': 48,
                'current_portfolio_value': 50,
                'transaction_type': 'withdrawal'
            },
            {
                'date': datetime(2020, 1, 3),
                'total_deposited': 48,
                'current_portfolio_value': 67,
                'transaction_type': 'update_portfolio_value'
            },
            {
                'date': datetime(2021, 1, 4),
                'total_deposited': 46,
                'current_portfolio_value': 65,
                'transaction_type': 'withdrawal'
            }
        ]
        self.test_portfolio.portfolio_history = test_data
        actual_output = self.mwr_calculator.calculate_return(self.test_portfolio,
                                                             annualised=False)
        # Example from: https://www.investopedia.com/terms/m/money-weighted-return.asp
        expected_output = 11.73
        self.assertEqual(actual_output, expected_output)

    def test_calculate_return_multi_deposits(self):
        # Test a multi-period portfolio with deposits only
        test_data = [
            {
                'date': datetime(2020, 1, 1),
                'total_deposited': 100,
                'current_portfolio_value': 100,
                'transaction_type': 'deposit'
            },
            {
                'date': datetime(2020, 3, 1),
                'total_deposited': 100,
                'current_portfolio_value': 110,
                'transaction_type': 'update_portfolio_value'
            },

            {
                'date': datetime(2020, 6, 1),
                'total_deposited': 100,
                'current_portfolio_value': 150,
                'transaction_type': 'update_portfolio_value'
            },
            {
                'date': datetime(2020, 1, 3),
                'total_deposited': 200,
                'current_portfolio_value': 250,
                'transaction_type': 'deposit'
            },
            {
                'date': datetime(2021, 1, 4),
                'total_deposited': 200,
                'current_portfolio_value': 400,
                'transaction_type': 'update_portfolio_value'
            },
            {
                'date': datetime(2021, 1, 5),
                'total_deposited': 300,
                'current_portfolio_value': 500,
                'transaction_type': 'deposit'
            }
        ]
        self.test_portfolio.portfolio_history = test_data
        actual_output = self.mwr_calculator.calculate_return(self.test_portfolio,
                                                             annualised=False)
        expected_output = round(irr([-100, -100, -100, 500]) * 100, 2)
        self.assertEqual(actual_output, expected_output)

    def test_calculate_return_negative_return(self):
        # Test a multi-period with negative return
        test_data = [
            {
                'date': datetime(2020, 1, 1),
                'total_deposited': 50,
                'current_portfolio_value': 50,
                'transaction_type': 'deposit'
            },
            {
                'date': datetime(2020, 3, 1),
                'total_deposited': 50,
                'current_portfolio_value': 30,
                'transaction_type': 'update_portfolio_value'
            },

            {
                'date': datetime(2020, 6, 1),
                'total_deposited': 100,
                'current_portfolio_value': 80,
                'transaction_type': 'deposit'
            },
            {
                'date': datetime(2020, 1, 3),
                'total_deposited': 100,
                'current_portfolio_value': 30,
                'transaction_type': 'update_portfolio_value'
            },
            {
                'date': datetime(2021, 1, 4),
                'total_deposited': 150,
                'current_portfolio_value': 80,
                'transaction_type': 'deposit'
            }
        ]
        self.test_portfolio.portfolio_history = test_data
        actual_output = self.mwr_calculator.calculate_return(self.test_portfolio,
                                                             annualised=False)
        expected_output = round(irr([-50, -50, -50, 80]) * 100, 2)
        self.assertEqual(actual_output, expected_output)


if __name__ == '__main__':
    unittest.main()
