"""
Contains db errors for project.

.. exception:: TgNoteBotDbError(TgNoteBotError)
.. exception:: UserAlreadyInDbError(TgNoteBotDbError)
"""

from ..errors import TgNoteBotError


class TgNoteBotDbError(TgNoteBotError):
    """
    Implements error for project db exceptions
    """


class UserAlreadyInDbError(TgNoteBotDbError):
    """
    Raised if user with the same id already exists in db
    """
