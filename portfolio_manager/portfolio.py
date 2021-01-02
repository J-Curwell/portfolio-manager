import abc
from datetime import datetime
from typing import Union, List


class InvestmentPortfolio:
    def __init__(self,
                 total_deposited: Union[int, float] = None,
                 current_portfolio_value: Union[int, float] = None,
                 portfolio_data: List[dict] = None):
        """
        To complete
        """
        self.total_deposited = total_deposited or 0
        self.current_portfolio_value = current_portfolio_value or 0
        self.portfolio_data = portfolio_data or []

    def deposit(self,
                deposit_amount: Union[int, float],
                date: datetime = None):
        # Make a deposit
        self.total_deposited += deposit_amount
        self.current_portfolio_value += deposit_amount
        date = date or datetime.now()

        # Update the portfolio_data
        self._update_portfolio_data(date)

    def withdraw(self,
                 withdrawal_amount: Union[int, float],
                 date: datetime = None):
        # Make a withdrawal
        self.total_deposited -= withdrawal_amount
        self.current_portfolio_value -= withdrawal_amount
        date = date or datetime.now()

        # Update the portfolio_data
        self._update_portfolio_data(date)

    def update_portfolio_value(self, current_portfolio_value: Union[int, float],
                               date: datetime = None):
        # Update the current total value of the assets in the portfolio
        self.current_portfolio_value = current_portfolio_value
        date = date or datetime.now()

        # Update the portfolio_data
        self._update_portfolio_data(date)

    def _update_portfolio_data(self, date):
        # Update the portfolio data
        new_entry = {
            'date': date,
            'total_deposited': self.total_deposited,
            'current_portfolio_value': self.current_portfolio_value
        }
        self.portfolio_data.append(new_entry)
        pass


class ReturnCalculator(abc.ABC):
    """ Consider putting this class in a different module """
    @abc.abstractmethod
    def calculate_return(self, portfolio: InvestmentPortfolio) -> Union[int, float]:
        pass
