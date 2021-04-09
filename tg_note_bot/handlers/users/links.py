"""
Contains user links handlers.
"""

import logging

from aiogram import types

# dp loading ^^^^^^^^^^^
from ...loader import dp
# ^^^^^^^^^^^^^^^^^^^^^^
from ...keyboards.reply import LinksAndRubricsMainKeyboard


logger = logging.getLogger(__name__)


@dp.message_handler(text=LinksAndRubricsMainKeyboard.text_for_button_to_see_links)
async def see_links(message: types.Message):
    """ Answer with list of the links"""

    # ------------------------------------------------------
    # fetch links
    # ------------------------------------------------------
    keyboard = LinksAndRubricsMainKeyboard(one_time_keyboard=True)

    await message.answer('It`s your links', reply_markup=keyboard)


@dp.message_handler(text=LinksAndRubricsMainKeyboard.text_for_button_to_see_links_by_rubric)
async def see_links_by_rubrics(message: types.Message):
    """ Answer with list of the links sorted by rubric """

    # ------------------------------------------------------
    # fetch links by rubric
    # ------------------------------------------------------
    keyboard = LinksAndRubricsMainKeyboard(one_time_keyboard=True)

    await message.answer('It`s your links by rubric', reply_markup=keyboard)


@dp.message_handler(text=LinksAndRubricsMainKeyboard.text_for_button_to_add_link)
async def add_link(message: types.Message):
    """ Add a new rubric """

    # ------------------------------------------------------
    # add link
    # ------------------------------------------------------
    keyboard = LinksAndRubricsMainKeyboard(one_time_keyboard=True)

    await message.answer('Adding not implemented', reply_markup=keyboard)


@dp.message_handler(text=LinksAndRubricsMainKeyboard.text_for_button_to_delete_link)
async def delete_rubric(message: types.Message):
    """ Delete the link """

    # ------------------------------------------------------
    # delete link
    # ------------------------------------------------------
    keyboard = LinksAndRubricsMainKeyboard(one_time_keyboard=True)

    await message.answer('Deleting not implemented', reply_markup=keyboard)
