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

    @staticmethod
    def calculate_annualised_return(portfolio: InvestmentPortfolio,
                                    total_return_percentage: Union[int, float]):
        """ To complete """
        portfolio_age = portfolio.get_portfolio_age()
        annualised_return = (1 + total_return_percentage / 100) ** (1 / portfolio_age)
        annualised_return_percentage = (annualised_return - 1) * 100
        return annualised_return_percentage


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
        return_percentage = (return_amount / portfolio.total_deposited) * 100

        if annualised:
            return_percentage = self.calculate_annualised_return(portfolio,
                                                                 return_percentage)

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
