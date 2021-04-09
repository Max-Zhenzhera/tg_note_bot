"""
Contains basis user handlers.
"""

import logging

from aiogram import types
from aiogram.dispatcher.filters import (
    CommandHelp,
    CommandStart
)

from ...keyboards.reply import LinksAndRubricsMainKeyboard
# dp loading ^^^^^^^^^^^
from ...loader import dp
# ^^^^^^^^^^^^^^^^^^^^^^


logger = logging.getLogger(__name__)


@dp.message_handler(CommandStart())
async def command_start(message: types.Message):
    """ Answer on start command """
    text = (
               f"Hello, {message.from_user.username}! "
               "I`m your small links saver bot:) Explore more with the /help command!"
    )
    keyboard = LinksAndRubricsMainKeyboard(one_time_keyboard=True)

    # ------------------------------------------------------
    # add user in db
    # ------------------------------------------------------

    await message.answer(text, reply_markup=keyboard)


@dp.message_handler(CommandHelp())
async def command_help(message: types.Message):
    """ Answer on help command """
    text = 'Not implemented'

    await message.answer("\n".join(text))


@dp.message_handler()
async def echo(message: types.Message):
    """ Echo """
    await message.answer(message.text)
