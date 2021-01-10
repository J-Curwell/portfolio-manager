import unittest
from unittest import mock
import sys
sys.path.append("..")
from portfolio_manager.portfolio import InvestmentPortfolio
from portfolio_manager.return_calculators import TimeWeightedReturnCalculator

class ReturnCalculatorsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.test_portfolio = InvestmentPortfolio(name="test_portfolio")
    
    def test_time_weighted_return(self):
        test_data =  [   
        {
            'date': '',
            'total_deposited': 100,
            'current_portfolio_value': 100,
            'transaction_type': ''
        },
        {
            'date': '',
            'total_deposited': 100,
            'current_portfolio_value': 110,
            'transaction_type': ''
        },
        {
            'date': '',
            'total_deposited': 200,
            'current_portfolio_value': 210,
            'transaction_type': ''
        },
        {
            'date': '',
            'total_deposited': 200,
            'current_portfolio_value': 215,
            'transaction_type': ''
        },
        {
            'date': '',
            'total_deposited': 250,
            'current_portfolio_value': 265,
            'transaction_type': ''
        },
        {
            'date': '',
            'total_deposited': 250,
            'current_portfolio_value': 280,
            'transaction_type': ''
        }
        ]
        self.test_portfolio.portfolio_history = test_data
        timeWeightedReturnCalculator = TimeWeightedReturnCalculator()
        actual_output = timeWeightedReturnCalculator.calculate_return(self.test_portfolio, annualised=False)
        expected_output = 18.99
        self.assertAlmostEqual(actual_output, expected_output)

if __name__ == '__main__':
    unittest.main()