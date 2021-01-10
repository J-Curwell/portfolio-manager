import abc
from datetime import datetime
from typing import Any, Union

import numpy
import pandas as pd

from portfolio_manager.portfolio import InvestmentPortfolio


class ReturnCalculator(abc.ABC):
    @abc.abstractmethod
    def calculate_return(self, portfolio: InvestmentPortfolio,
                         annualised: bool) -> Any:
        pass

    def calculate_annualised_return(self, total_return_percentage: Union[int, float],
                                    start: datetime, end: datetime):
        """ To complete """
        n_years = self.calculate_n_years(start, end)
        annualised_return = (1 + total_return_percentage/100) ** (1 / n_years)
        annualised_return_percentage = (annualised_return - 1) * 100
        return annualised_return_percentage

    @staticmethod
    def calculate_n_years(start: datetime, end: datetime) -> Union[int, float]:
        delta = end - start
        return delta.days/365


class StandardReturnCalculator(ReturnCalculator):
    """
    Calculate the percentage return of the portfolio using the following formula:

    ((current portfolio value - total amount deposited) / total amount deposited) * 100

    ...

    """
    def calculate_return(self, portfolio: InvestmentPortfolio,
                         annualised: bool = True) -> Any:
        """ To complete """
        return_amount = portfolio.current_portfolio_value - portfolio.total_deposited
        return_percentage = (return_amount/portfolio.total_deposited) * 100

        if annualised:
            # Use the fact that the portfolio history is ordered by transaction date
            portfolio_history = portfolio.portfolio_history
            start = portfolio_history[0]['date']
            end = portfolio_history[-1]['date']
            return_percentage = self.calculate_annualised_return(return_percentage,
                                                                 start,
                                                                 end)

        return return_percentage


class TimeWeightedReturnCalculator(ReturnCalculator):
    """ To complete """
    def calculate_return(self, portfolio: InvestmentPortfolio,
                         annualised: bool = True) -> Any:
        # If there isn't enough data in the portfolio, return 0
        if len(portfolio.portfolio_history) <= 1:
            return 0

        # Otherwise, calculate the time-weighted return
        sub_period_returns = []
        portfolio_data = pd.DataFrame(portfolio.portfolio_history)

        # Group the data into sub-periods. Identify these sub-periods by finding all
        # consecutive transactions with the same 'total_deposited' values
        is_new_period_ser = pd.Series((portfolio_data['total_deposited'].shift() !=
                                       portfolio_data['total_deposited']))
        grouped_periods = portfolio_data.groupby(is_new_period_ser.cumsum())

        # Loop through each sub-period to calculate the returns for that period
        for subperiod, data in grouped_periods:
            subperiod_data = pd.DataFrame(data)

            start_value = subperiod_data['current_portfolio_value'].values[0]
            end_value = subperiod_data['current_portfolio_value'].values[-1]

            return_for_period = (end_value - start_value) / start_value
            sub_period_returns.append(return_for_period + 1)

        twr_return_percentage = (numpy.prod(sub_period_returns) - 1) * 100

        if annualised:
            start = portfolio.portfolio_history[0]['date']
            end = portfolio.portfolio_history[-1]['date']
            twr_return_percentage = self.calculate_annualised_return(
                twr_return_percentage, start, end)

        return round(twr_return_percentage, 2)
