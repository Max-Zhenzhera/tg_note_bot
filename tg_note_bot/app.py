"""
Contains main function for running.

Upgrades dp with all stuff (handlers, middlewares, ...) by imports.

.. func:: main
    Run the bot
"""

from aiogram import (
    Dispatcher,
    executor
)

# fresh up dp | | | | | | | | | | | | | | | | | | | | | | | | | | |
from .loader import dp
from .handlers import dp
from .middlewares import dp
# | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
from .utils.admins_notifying import notify_admins_on_startup


async def on_startup(dp: Dispatcher):
    await notify_admins_on_startup(dp)


def main():
    """ Run the bot """
    executor.start_polling(dp, on_startup=on_startup)
