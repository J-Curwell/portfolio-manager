from datetime import datetime
from typing import Union
import abc

from pandas import DataFrame


class ReturnCalculator(abc.ABC):
    @abc.abstractmethod
    def calculate_return(self, porfolio_data: DataFrame) -> Union[int, float]:
        pass


class InvestmentPortfolio:
    def __init__(self,
                 total_deposited: Union[int, float],
                 current_portfolio_value: Union[int, float],
                 percentage_return: Union[int, float],
                 portfolio_data: DataFrame):
        """
        To complete
        """
        self.total_deposited = total_deposited
        self.current_portfolio_value = current_portfolio_value
        self.percentage_return = percentage_return
        self.portfolio_data = portfolio_data

    def deposit(self,
                amount: Union[int, float],
                current_portfolio_value: Union[int, float] = None,
                date: datetime = None):
        # Make a deposit
        self.total_deposited += amount
        if current_portfolio_value:
            self.current_portfolio_value = current_portfolio_value
        if date is None:
            data = datetime.now()

    def calculate_return(self):
        # Calculate the percentage_return of the current portfolio
        pass

    def print_porfolio_breakdown(self):
        # Print a breakdown of the current portfolio
        pass

    def _update_portfolio_data(self):
        # Update the portfolio data
        df = self.portfolio_data
        pass
