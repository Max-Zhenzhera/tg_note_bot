"""
Contains middlewares. Also it is possible to setup them here on the fly.
"""

from .throttling import ThrottlingMiddleware
from ..loader import dp
from ..settings import THROTTLING_RATE_LIMIT_IN_SECONDS


if __name__ != "__main__":
    import logging

    logger = logging.getLogger(__name__)

    dp.middleware.setup(ThrottlingMiddleware(limit=THROTTLING_RATE_LIMIT_IN_SECONDS))

    logger.debug('Middlewares has been installed')
