import abc
from typing import Any, Union
from portfolio_manager.portfolio import InvestmentPortfolio
import numpy


class ReturnCalculator(abc.ABC):
    @abc.abstractmethod
    def calculate_return(self, portfolio: InvestmentPortfolio,
                         annualised: bool) -> Any:
        pass


    @staticmethod
    def calculate_annualised_return(total_return_percentage: Union[int, float],
                                    n_years: Union[int, float]):
        """ To complete """
        annualised_return = (1 + total_return_percentage/100) ** (1 / n_years)
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
        return_percentage = (return_amount/portfolio.total_deposited) * 100

        if annualised:
            return_percentage = self.calculate_annualised_return(return_percentage, 3)

        return return_percentage


class TimeWeightedReturnCalculator(ReturnCalculator):
    """ To complete """
    def calculate_return(self, portfolio: InvestmentPortfolio,
                         annualised: bool = True) -> Any:
        HP = []
        sorted_portfolio_history = sorted(portfolio.portfolio_history, key=lambda k: k['date'])
        if len(sorted_portfolio_history) <= 1:
            twr_return_percentage=0
        else:
            for i in range(len(sorted_portfolio_history) - 1):
                total_deposited = sorted_portfolio_history[i]['total_deposited']
                if total_deposited != sorted_portfolio_history[i+1]['total_deposited']:
                    cash_flow = sorted_portfolio_history[i+1]['total_deposited'] - sorted_portfolio_history[i]['total_deposited']
                    end_value = sorted_portfolio_history[i+1]['current_portfolio_value'] - cash_flow

                # inital_value = sorted_portfolio_history[i]['current_portfolio_value']
                # end_value = sorted_portfolio_history[i+1]['current_portfolio_value']
                # cash_flow = sorted_portfolio_history[i+1]['total_deposited'] - sorted_portfolio_history[i]['total_deposited']
                # return_for_period = (end_value - inital_value + cash_flow) / (inital_value + cash_flow)
                # HP.append(1 + return_for_period)
            twr_return_percentage = (numpy.prod(HP) - 1) * 100
            if annualised:
                pass
        return twr_return_percentage
