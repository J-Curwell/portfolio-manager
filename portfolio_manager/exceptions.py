class PortfolioError(Exception):
    """ Base class for handling exceptions related to investment portfolios. """
    pass


class BackDatingError(PortfolioError):
    """ Attempting to make transactions in the wrong order. """
    pass


class InsufficientData(PortfolioError):
    """ There have been too few portfolio transactions to perform the desired action. """
    pass


class InsufficientFunds(PortfolioError):
    """ There are insufficient funds in the portfolio to perform the desired action. """
    pass
