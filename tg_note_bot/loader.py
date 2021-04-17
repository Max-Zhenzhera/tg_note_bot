"""
Contains all objects that might be imported from child packages (handlers, ...).
- This is a quick way to fresh up dp -> in the second step import from other modules upgraded dp.

.. data:: bot
.. data:: bot
.. data:: storage
.. data:: async_db_sessionmaker
"""

from aiogram import (
    Bot,
    Dispatcher,
    types
)
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from . import settings
from .db import postgres
from .settings import (
    LOGGING_CONFIG_PATH,
    REDIS_HOST,
    REDIS_PORT
)
from .utils.logging_ import setup_logging


__all__ = ['dp', 'async_db_sessionmaker']


# logging setting - - - - - - - - - - - - -
setup_logging(LOGGING_CONFIG_PATH)
# - - - - - - - - - - - - - - - - - - - - -


# objects for importing - - - - - - - - - - - - - - - - - - - - - - -
# # bot
bot = Bot(token=settings.BOT_TOKEN, parse_mode=types.ParseMode.HTML)

storage = RedisStorage2(REDIS_HOST, REDIS_PORT)
dp = Dispatcher(bot=bot, storage=storage)
# # db
async_db_sessionmaker = postgres.create_db_session()
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
