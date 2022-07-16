class BotException(Exception):
    pass


class NoConnectionWith1c(BotException):
    """No connection withs 1c"""


class NoAuthentication(BotException):
    """No Authentication"""


class NoValidationData(BotException):
    """No Authentication"""
