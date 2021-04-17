"""
Contains test handlers.

.. async:: test_command(message: types.Message) -> None
"""

from aiogram import types
from aiogram.utils import markdown as md

from ...loader import dp


@dp.message_handler(commands=['test'])
async def test_command(message: types.Message) -> None:
    """ Answer on help command """
    await message.answer('Test')
