"""
Contains handlers for serious deleting.

"""

import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils import markdown as md

from ... import db
from ...keyboards.reply import LinksAndRubricsMainReplyKeyboard
from ...loader import (
    dp,
    async_db_sessionmaker
)


logger = logging.getLogger(__name__)


