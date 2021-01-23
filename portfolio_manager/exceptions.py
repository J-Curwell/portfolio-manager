class PortfolioError(Exception):
    """ Base class for handling exceptions related to investment portfolios. """
    pass


class BackDatingError(PortfolioError):
    """ Attempting to back-date a transaction too far into the past. """
    pass


class InsufficientData(PortfolioError):
    """ There have been too few portfolio transactions to perform the desired action. """
    pass


class InsufficientFunds(PortfolioError):
    """ There are insufficient funds in the portfolio to perform the desired action. """
    pass
