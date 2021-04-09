"""
Contains all objects that might be imported from child packages (handlers, ...).
- This is a quick way to fresh up dp -> in the second step import from other modules upgraded dp.

.. data:: bot
.. data:: dp
.. data:: async_db_session
"""

from aiogram import (
    Bot,
    Dispatcher,
    types
)
# from aiogram.contrib.fsm_storage.memory import MemoryStorage

from . import settings
from .db import sqlite
from .settings import LOGGING_CONFIG_PATH
from .utils.logging_ import setup_logging


# logging setting - - - - - - - - - - - - -
setup_logging(LOGGING_CONFIG_PATH)
# - - - - - - - - - - - - - - - - - - - - -


# objects for importing - - - - - - - - - - - - - - - - - - - - - - -
# # bot
bot = Bot(token=settings.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

# # bot state storage
# storage = MemoryStorage()

# # db
async_db_session = sqlite.create_db_session()
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
