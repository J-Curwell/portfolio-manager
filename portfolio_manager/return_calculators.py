import abc
from typing import Any, Union

import numpy
import pandas as pd

from portfolio_manager.portfolio import InvestmentPortfolio


class ReturnCalculator(abc.ABC):
    @abc.abstractmethod
    def calculate_return(self, portfolio: InvestmentPortfolio,
                         annualised: bool) -> Any:
        pass

    def calculate_annualised_return(self, portfolio: InvestmentPortfolio,
                                    total_return_percentage: Union[int, float]):
        """
        Given the overall return percentage of a portfolio, calculate the annualised
        return percentage.
        """
        portfolio_age = self.get_portfolio_age(portfolio)
        annualised_return = (1 + total_return_percentage / 100) ** (1 / portfolio_age)
        annualised_return_percentage = (annualised_return - 1) * 100
        return round(annualised_return_percentage, 2)

    @staticmethod
    def get_portfolio_age(portfolio: InvestmentPortfolio,
                          unit: str = None) -> Union[int, float]:
        """
        Calculate the 'age' of a portfolio. This is the difference in time between the
        first transaction in the portfolio and the most recent one.

        Parameters
        ----------
        portfolio : InvestmentPortfolio
            The portfolio we are calculating the age of.
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
        start = portfolio.portfolio_history[0]['date']
        end = portfolio.portfolio_history[-1]['date']
        delta = end - start

        if unit == 'days':
            # Round to the nearest integer
            return round(delta.days, 0)

        if unit == 'months':
            # Round to the nearest integer
            return round((delta.days / 365) * 12, 0)

        # By default, return the portfolio age in years, rounded to the nearest 2 d.p's
        if unit == 'years' or unit is None:
            return round(delta.days / 365, 2)


class SimpleReturnCalculator(ReturnCalculator):
    """
    Calculate the simple percentage return of a portfolio using the following formula:

    ((current portfolio value - total amount deposited) / total amount deposited) * 100

    Note: If, due to a combination of deposits and withdrawals, the total amount
    deposited in the portfolio is <= 0 then this value will be meaningless. In this case,
    a TimeWeightedReturnCalculator is a better choice.
    """
    def calculate_return(self, portfolio: InvestmentPortfolio,
                         annualised: bool = True) -> Any:
        """
        Calculate the simple rate of return of the portfolio.

        Parameters
        ----------
        portfolio : InvestmentPortfolio
            The portfolio we are calculating the simple return for.
        annualised : bool
            If True, calculate the annualised return.

        Returns
        -------
        Any : The simple rate of return of the portfolio, as a percentage.
            e.g. 18 represents 18%.
        """
        # If there isn't enough data in the portfolio, raise an error
        if len(portfolio.portfolio_history) <= 1:
            raise ValueError('Not enough portfolio data to calculate a return.')

        # If the sum of all deposits and withdrawals is negative or zero, raise an error
        if portfolio.total_deposited <= 0:
            raise ValueError('Total deposited is negative or zero.')

        return_amount = portfolio.current_portfolio_value - portfolio.total_deposited
        return_percentage = (return_amount / portfolio.total_deposited) * 100

        if annualised:
            return_percentage = self.calculate_annualised_return(portfolio,
                                                                 return_percentage)

        return round(return_percentage, 2)


class TimeWeightedReturnCalculator(ReturnCalculator):
    """
    Calculate the time-weighted rate of return of a portfolio. This metric is useful for
    measuring the performance of a portfolio where many deposits/withdrawals have been
    paid over time. See for more information
    """
    def calculate_return(self, portfolio: InvestmentPortfolio,
                         annualised: bool = True) -> Any:
        """
        Calculate the time-weighted rate of return of the portfolio.

        Parameters
        ----------
        portfolio : InvestmentPortfolio
            The portfolio we are calculating the time-weighted return for.
        annualised : bool
            If True, calculate the annualised return.

        Returns
        -------
        Any : The time-weighted rate of return of the portfolio, as a percentage.
            e.g. 18 represents 18%.
        """
        # If there isn't enough data in the portfolio, raise an error
        if len(portfolio.portfolio_history) <= 1:
            raise ValueError('Not enough portfolio data to calculate a return.')

        # Otherwise, calculate the time-weighted return
        sub_period_returns = []
        df = pd.DataFrame(portfolio.portfolio_history)

        # Group the data into sub-periods. Identify these sub-periods by finding groups
        # of consecutive transactions with the same 'total_deposited' values
        is_new_period_ser = pd.Series(
            df['total_deposited'].shift() != df['total_deposited'])
        grouped_periods = df.groupby(is_new_period_ser.cumsum())

        # Loop through each sub-period to calculate the returns for that period
        for _, data in grouped_periods:
            sub_period_data = pd.DataFrame(data)

            start_value = sub_period_data['current_portfolio_value'].values[0]
            end_value = sub_period_data['current_portfolio_value'].values[-1]

            return_for_period = (end_value - start_value) / start_value
            sub_period_returns.append(return_for_period + 1)

        twr_return_percentage = (numpy.prod(sub_period_returns) - 1) * 100

        if annualised:
            twr_return_percentage = self.calculate_annualised_return(
                portfolio, twr_return_percentage)

        return round(twr_return_percentage, 2)
