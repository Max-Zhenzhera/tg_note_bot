"""
Contains functions for admins notifying.
"""

import logging

from aiogram import Dispatcher

from ..settings import ADMINS


logger = logging.getLogger(__name__)


async def notify_admins_on_startup(dp: Dispatcher) -> None:
    """
    Send message to admins on startup.

    :param dp: bot dispatcher
    :type dp: Dispatcher

    :return: None
    :rtype: None
    """

    message = '🏳️ Bot is running!'

    for admin in ADMINS:
        try:
            await dp.bot.send_message(admin, message)

            logger.debug(f'Admin with id <{admin}> has been notified about startup')
        except Exception as error:
            logger.exception(msg=str(error), exc_info=error)
        else:
            logger.info('Admins have been notified on startup')
