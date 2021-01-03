import abc
from typing import Any, Union

from portfolio_manager.portfolio import InvestmentPortfolio


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
        pass
