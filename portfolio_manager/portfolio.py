import pickle
from datetime import datetime
from typing import Union, List


class InvestmentPortfolio:
    def __init__(self,
                 name: str = None,
                 total_deposited: Union[int, float] = None,
                 current_portfolio_value: Union[int, float] = None,
                 portfolio_history: List[dict] = None):
        """
        Represents an investment portfolio. Funds can be deposited/withdrawn, and the
        current value of the assets in the portfolio can be updated over time. Historical
        transactions and value changes are saved.

        Parameters
        ----------
        name : str
            The name of the portfolio. Defaults to 'portfolio_{today's date}'.
        total_deposited : Union[int, float]
            The total amount that has been invested into the portfolio. i.e. the sum of
            each individual deposit.
        current_portfolio_value : Union[int, float]
            The current total value of all the assets within the portfolio.
        portfolio_history : List[dict]
            Stores historical portfolio data by saving a snapshot of the portfolio each
            time it is updated. Each snapshot is a dictionary with keys 'date',
            'total_deposited', 'current_portfolio_value' and 'transaction_type'.
        """
        date_today = datetime.now().strftime('%d%m%Y')
        self.name = name or f'portfolio_{date_today}'
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
        self._update_portfolio_history(date, 'deposit')

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
        self._update_portfolio_history(date, 'withdrawal')

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
        self._update_portfolio_history(date, 'update_portfolio_value')

    def _update_portfolio_history(self, date: datetime, transaction_type: str):
        """
        Add a snapshot of the current portfolio to portfolio_history.

        Parameters
        ----------
        date : datetime
            The date at which the portfolio snapshot was taken.
        transaction_type : str
            The type of transaction that was made before taking the portfolio snapshot.
        """
        # Update portfolio_history
        new_entry = {
            'date': date,
            'total_deposited': self.total_deposited,
            'current_portfolio_value': self.current_portfolio_value,
            'transaction_type': transaction_type
        }
        self.portfolio_history.append(new_entry)

    def save_portfolio(self, directory: str = None):
        """
        Save the state of a portfolio

        ...

        """
        path = f'{directory}/{self.name}.pkl' if directory else f'{self.name}.pkl'

        # Save the portfolio, overwriting any existing files at that path.
        with open(path, 'wb') as handle:
            pickle.dump(self, handle, pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def load_portfolio(path: str = None):
        """ To complete """
        # Load the portfolio
        with open(path, 'rb') as handle:
            portfolio = pickle.load(handle)
        return portfolio
