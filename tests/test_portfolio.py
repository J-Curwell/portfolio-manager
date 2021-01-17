import unittest
from datetime import datetime
from unittest import mock

from portfolio_manager.portfolio import InvestmentPortfolio


class InvestmentPortfolioTests(unittest.TestCase):
    def setUp(self) -> None:
        self.test_portfolio = InvestmentPortfolio(name="test_portfolio")

    def test_init(self):
        self.assertIsInstance(self.test_portfolio, InvestmentPortfolio)
        self.assertEqual("test_portfolio", self.test_portfolio.name)
        self.assertEqual(0, self.test_portfolio.total_deposited)
        self.assertEqual(0, self.test_portfolio.current_portfolio_value)
        self.assertListEqual([], self.test_portfolio.portfolio_history)

    def test_deposit(self):
        # Deposit £22.50 using a specified datetime
        past = datetime(2021, 1, 1)
        self.test_portfolio.deposit(22.5, date=past)
        self.assertEqual(22.5, self.test_portfolio.total_deposited)
        self.assertEqual(22.5, self.test_portfolio.current_portfolio_value)

        # Deposit a further £27.50 using the default datetime and updating the portfolio
        # value before the deposit. To avoid time issues, we patch the value of the
        # default datetime, which is datetime.now()
        with mock.patch('portfolio_manager.portfolio.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2021, 2, 1)
            self.test_portfolio.deposit(27.5, portfolio_value_before_deposit=25)
        self.assertEqual(50, self.test_portfolio.total_deposited)
        self.assertEqual(52.5, self.test_portfolio.current_portfolio_value)

        # Check the two deposits and one value update were successfully recorded
        expected_transaction_history = [{'date': past,
                                         'total_deposited': 22.5,
                                         'current_portfolio_value': 22.5,
                                         'transaction_type': 'deposit'},
                                        {'date': datetime(2021, 2, 1),
                                         'total_deposited': 22.5,
                                         'current_portfolio_value': 25,
                                         'transaction_type': 'update_portfolio_value'},
                                        {'date': datetime(2021, 2, 1),
                                         'total_deposited': 50,
                                         'current_portfolio_value': 52.5,
                                         'transaction_type': 'deposit'}]
        self.assertListEqual(expected_transaction_history,
                             self.test_portfolio.portfolio_history)

        # Test that trying to incorrectly back-date a deposit raises an error
        with self.assertRaises(ValueError):
            self.test_portfolio.deposit(22.5, date=past)

    def test_withdraw(self):
        # Test that trying to withdraw more money than is available raises an error
        with self.assertRaises(ValueError):
            self.test_portfolio.withdraw(10)

        # Deposit some funds to avoid the above error for the remaining tests
        self.test_portfolio.deposit(50, date=datetime(2021, 1, 1))

        # Test that trying to incorrectly back-date a withdrawal raises an error
        with self.assertRaises(ValueError):
            self.test_portfolio.withdraw(10, date=datetime(2020, 1, 1))

        # Test withdrawing 10 from a specified date
        self.test_portfolio.withdraw(10, date=datetime(2021, 1, 2))
        self.assertEqual(40, self.test_portfolio.total_deposited)
        self.assertEqual(40, self.test_portfolio.current_portfolio_value)

        # Withdraw a further £12.50 using the default datetime and updating the portfolio
        # value before the withdrawal. To avoid time issues, we patch the value of the
        # default datetime, which is datetime.now()
        with mock.patch('portfolio_manager.portfolio.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2021, 2, 1)
            self.test_portfolio.withdraw(12.5, portfolio_value_before_withdrawal=25)
        self.assertEqual(27.50, self.test_portfolio.total_deposited)
        self.assertEqual(12.50, self.test_portfolio.current_portfolio_value)

        # Check the successful transactions were recorded correctly
        expected_transaction_history = [{'date': datetime(2021, 1, 1),
                                         'total_deposited': 50,
                                         'current_portfolio_value': 50,
                                         'transaction_type': 'deposit'},
                                        {'date': datetime(2021, 1, 2),
                                         'total_deposited': 40,
                                         'current_portfolio_value': 40,
                                         'transaction_type': 'withdrawal'},
                                        {'date': datetime(2021, 2, 1),
                                         'total_deposited': 40,
                                         'current_portfolio_value': 25,
                                         'transaction_type': 'update_portfolio_value'},
                                        {'date': datetime(2021, 2, 1),
                                         'total_deposited': 27.50,
                                         'current_portfolio_value': 12.5,
                                         'transaction_type': 'withdrawal'}]
        self.assertListEqual(expected_transaction_history,
                             self.test_portfolio.portfolio_history)


if __name__ == "__main__":
    unittest.main()
