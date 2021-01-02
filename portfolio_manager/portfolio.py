import abc
from datetime import datetime
from typing import Union, List, Any


class InvestmentPortfolio:
    def __init__(self,
                 total_deposited: Union[int, float] = None,
                 current_portfolio_value: Union[int, float] = None,
                 portfolio_history: List[dict] = None):
        """
        Represents an investment portfolio. Funds can be deposited/withdrawn, and the
        current value of the assets in the portfolio can be updated over time. Historical
        transactions and value changes are saved.

        Parameters
        ----------
        total_deposited : Union[int, float]
            The total amount that has been invested into the portfolio. i.e. the sum of
            each individual deposit.
        current_portfolio_value : Union[int, float]
            The current total value of all the assets within the portfolio.
        portfolio_history : List[dict]
            Stores historical portfolio data by saving a snapshot of the portfolio each
            time it is updated. Each snapshot is a dictionary with keys 'date',
            'total_deposited' and 'current_portfolio_value'.
        """
        self.total_deposited = total_deposited or 0
        self.current_portfolio_value = current_portfolio_value or 0
        self.portfolio_history = portfolio_history or []

    def deposit(self,
                deposit_amount: Union[int, float],
                date: datetime = None):
        """
        Deposit funds into the portfolio.

        Parameters
        ----------
        deposit_amount : Union[int, float]
            The amount of money being deposited into the portfolio.
        date : datetime
            When the deposit was made. Defaults to now.
        """
        # Update the total amount deposited and the current portfolio value
        self.total_deposited += deposit_amount
        self.current_portfolio_value += deposit_amount
        date = date or datetime.now()

        # Update portfolio_history
        self._update_portfolio_history(date)

    def withdraw(self,
                 withdrawal_amount: Union[int, float],
                 date: datetime = None):
        """
        Deposit additional funds into the portfolio.

        Parameters
        ----------
        withdrawal_amount : Union[int, float]
            The amount of money being withdrawn from the portfolio.
        date : datetime
            When the withdrawal was made. Defaults to now.
        """
        # Update the total amount deposited and the current portfolio value
        self.total_deposited -= withdrawal_amount
        self.current_portfolio_value -= withdrawal_amount
        date = date or datetime.now()

        # Update portfolio_history
        self._update_portfolio_history(date)

    def update_portfolio_value(self, current_portfolio_value: Union[int, float],
                               date: datetime = None):
        """
        Update the current value of all assets in the portfolio.

        Parameters
        ----------
        current_portfolio_value : Union[int, float]
            The current total value of all assets in the portfolio.
        date : datetime
            When this valuation was calculated. Defaults to now.
        """
        # Update the current total value of the assets in the portfolio
        self.current_portfolio_value = current_portfolio_value
        date = date or datetime.now()

        # Update portfolio_history
        self._update_portfolio_history(date)

    def _update_portfolio_history(self, date: datetime):
        """
        Add a snapshot of the current portfolio to portfolio_history.

        Parameters
        ----------
        date : datetime
            The date at which the portfolio snapshot was taken.
        """
        # Update portfolio_history
        new_entry = {
            'date': date,
            'total_deposited': self.total_deposited,
            'current_portfolio_value': self.current_portfolio_value
        }
        self.portfolio_history.append(new_entry)


class ReturnCalculator(abc.ABC):
    """ Consider putting this class in a different module """
    @abc.abstractmethod
    def calculate_return(self, portfolio: InvestmentPortfolio) -> Any:
        pass
