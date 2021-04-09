"""
Contains basis user handlers.
"""

from aiogram import types
from aiogram.dispatcher.filters import (
    CommandHelp,
    CommandStart
)

from ...loader import dp
import logging


logger = logging.getLogger(__name__)


@dp.message_handler(CommandStart())
async def command_start(message: types.Message):
    """ Answer on start command """
    text = (
               f"Hello, {message.from_user.username}! "
               "I`m your small links saver bot:) Explore more with the /help command!"
    )

    await message.answer(text)


@dp.message_handler(CommandHelp())
async def command_help(message: types.Message):
    """ Answer on help command """
    text = (
        "List of the commands:",
        "\t/{command:<10} - to commence working with me;".format(command='start'),
        "\t/{command:<10} - to commence working with me;".format(command='help')
    )

    await message.answer("\n".join(text))


@dp.message_handler()
async def echo(message: types.Message):
    """ Echo """
    await message.answer(message.text)
