class PortfolioError(Exception):
    """ Base class for handling exceptions related to investment portfolios. """
    pass


class BackDatingError(PortfolioError):
    """
    Attempting to back-date a transaction too far into the past. Transactions can not be
    back-dated to further back than the most recent transaction. This is to prevent
    issues with inserting transactions which make future transactions invalid.

    e.g. If the most recent transaction was made on 1st Jan 2021 12:00pm, then a
        transaction can be back-dated to 1st Jan 2021 12:01pm, but no earlier.
    """
    pass


class InsufficientData(PortfolioError):
    """
    There have been too few portfolio transactions to perform the desired action.

    e.g. When attempting to make a withdrawal before the first deposit has been made.
    """
    pass


class InsufficientFunds(PortfolioError):
    """
    There are insufficient funds in the portfolio to perform the desired action.

    e.g. Attempting to withdraw £100 when the portfolio value is only £80.
    """
    pass
