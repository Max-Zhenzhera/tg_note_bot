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
from .commands import COMMANDS
from .utils.admins_notifying import notify_admins_on_startup


async def on_startup(dp: Dispatcher) -> None:
    await notify_admins_on_startup(dp)

    await dp.bot.set_my_commands(COMMANDS)


async def on_shutdown(dp: Dispatcher) -> None:
    # close storage
    await dp.storage.close()
    await dp.storage.wait_closed()


def main():
    """ Run the bot """
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
