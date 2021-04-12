"""
Contains test handlers.
"""

from aiogram import types
from aiogram.utils import markdown as md

from ...loader import dp


@dp.message_handler(commands=['test'])
async def test_command(message: types.Message):
    """ Answer on help command """
    a = 'https://www.youtube.com/watch?v=K70nC0FbxiU&list=RDMM9fUyul2Hg18&index=27'
    await message.answer(a, disable_web_page_preview=True)
