"""
Contains all objects that might be imported in child packages (handlers, ...).

.. data:: bot
.. data:: dp
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
from .db.postgres import async_db_sessionmaker
from .settings import (
    LOGGING_CONFIG_PATH,
    REDIS_CONFIG
)
from .utils.logging_ import setup_logging


__all__ = ['dp', 'async_db_sessionmaker']


# logging setting - - - - - - - - - - - - -
setup_logging(LOGGING_CONFIG_PATH)
# - - - - - - - - - - - - - - - - - - - - -


# objects for importing - - - - - - - - - - - - - - - - - - - - - - -
# # bot-dp
bot = Bot(token=settings.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = RedisStorage2(**REDIS_CONFIG)
dp = Dispatcher(bot=bot, storage=storage)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
