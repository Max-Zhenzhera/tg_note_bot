"""
Contains main function for running.

Upgrades dp with all stuff (handlers, middlewares, ...) by imports.

.. func:: main
    Run the bot
"""

from aiogram import executor

# fresh up dp
from .loader import dp
from .handlers import dp
from .middlewares import dp


# from utils.notify_admins import on_startup_notify
#
# async def on_startup(dispatcher):
#     # Уведомляет про запуск
#     await on_startup_notify(dispatcher)


def main():
    """ Run the bot """

    executor.start_polling(dp)
