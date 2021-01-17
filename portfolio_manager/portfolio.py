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
                portfolio_value_before_deposit: Union[int, float] = None,
                date: datetime = None):
        """
        Deposit funds into the portfolio.

        Parameters
        ----------
        deposit_amount : Union[int, float]
            The amount of money being deposited into the portfolio.
        portfolio_value_before_deposit : Union[int, float]
            The total value of the portfolio before making the deposit.
        date : datetime
            When the deposit was made. Defaults to now.
        """
        # Update the portfolio value from before the deposit, if this value is provided
        if portfolio_value_before_deposit:
            self.update_portfolio_value(portfolio_value_before_deposit, date)

        # Update the total amount deposited and current portfolio value
        self.total_deposited += deposit_amount
        self.current_portfolio_value += deposit_amount

        # Update portfolio_history
        self._update_portfolio_history(date, 'deposit')

    def withdraw(self,
                 withdrawal_amount: Union[int, float],
                 portfolio_value_before_withdrawal: Union[int, float] = None,
                 date: datetime = None):
        """
        Deposit additional funds into the portfolio.

        Parameters
        ----------
        withdrawal_amount : Union[int, float]
            The amount of money being withdrawn from the portfolio.
        portfolio_value_before_withdrawal : Union[int, float]
            The total value of the portfolio before making the withdrawal.
        date : datetime
            When the withdrawal was made. Defaults to now.
        """
        # Update the portfolio value from before the deposit, if this value is provided
        if portfolio_value_before_withdrawal:
            self.update_portfolio_value(portfolio_value_before_withdrawal, date)

        # Update the total amount deposited and the current portfolio value
        self.total_deposited -= withdrawal_amount
        self.current_portfolio_value -= withdrawal_amount

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
        # The default transaction date is now
        date = date or datetime.now()

        # Update portfolio_history
        new_entry = {
            'date': date,
            'total_deposited': self.total_deposited,
            'current_portfolio_value': self.current_portfolio_value,
            'transaction_type': transaction_type
        }
        portfolio_history = self.portfolio_history
        portfolio_history.append(new_entry)

        # Ensure the portfolio history is stored in order of ascending transaction date
        sorted_portfolio_history = sorted(portfolio_history, key=lambda x: x['date'])
        self.portfolio_history = sorted_portfolio_history

    def get_portfolio_age(self, unit: str = None) -> Union[int, float]:
        """
        Calculate the 'age' of the portfolio. This is the difference in time between the
        first transaction in the portfolio and the most recent one.

        Parameters
        ----------
        unit : str
            The desired unit of time for portfolio age to be calculated in. Defaults to
            years but can also be 'months' or 'days'.

        Returns
        -------
        Union[int, float]: The age of the portfolio measure in the specified unit of
            time, or years by default.
        """
        # Here we make use of the fact that the transactions within portfolio history
        # are ordered by ascending date
        start = self.portfolio_history[0]['date']
        end = self.portfolio_history[-1]['date']
        delta = end - start

        if unit == 'days':
            return delta.days

        if unit == 'months':
            return delta.days/12

        # By default, return the portfolio age in years
        return delta.days/365

    def save_portfolio(self, directory: str = None):
        """
        Save the state of the current portfolio. The portfolio object is pickled and
        saved within the specified directory under the name '{self.name}.pkl'.

        Parameters
        ----------
        directory : str
            The directory that the pickled object should be saved in. Defaults to the
            current working directory.
        """
        path = f'{directory}/{self.name}.pkl' if directory else f'{self.name}.pkl'

        # Save the portfolio, overwriting any existing files at that path.
        with open(path, 'wb') as handle:
            pickle.dump(self, handle, pickle.HIGHEST_PROTOCOL)


def load_portfolio(name: str, directory: str = None) -> InvestmentPortfolio:
    """
    Load a previously pickled and saved portfolio from the specified path.

    Parameters
    ----------
    name : str
        The name of the portfolio being loaded. i.e. the 'name' attribute of the saved
        portfolio object.
    directory : str
        The directory containing the saved portfolio. By default, look in the current
        working directory.

    Returns
    -------
    InvestmentPortfolio : The instantiated portfolio object.
    """
    # Add the .pkl file extension if it isn't already there
    if '.' not in name:
        name += '.pkl'

    # Load and return the portfolio
    path = f'{directory}/{name}' if directory else name
    with open(path, 'rb') as handle:
        portfolio = pickle.load(handle)

    return portfolio
