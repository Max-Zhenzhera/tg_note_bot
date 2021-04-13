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
    a = md.hbold('✅')
    b = types.InlineKeyboardMarkup()
    b.add(types.InlineKeyboardButton(a, callback_data='123'))
    await message.answer('test', reply_markup=b)

