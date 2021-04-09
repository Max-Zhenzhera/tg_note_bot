"""
Contains user rubrics handlers.
"""

import logging

from aiogram import types

# dp loading ^^^^^^^^^^^
from ...loader import dp
# ^^^^^^^^^^^^^^^^^^^^^^
from ...keyboards.reply import LinksAndRubricsMainKeyboard


logger = logging.getLogger(__name__)


@dp.message_handler(text=LinksAndRubricsMainKeyboard.text_for_button_to_see_rubrics)
async def see_rubrics(message: types.Message):
    """ Answer with list of the rubrics"""

    # ------------------------------------------------------
    # fetch rubrics
    # ------------------------------------------------------
    keyboard = LinksAndRubricsMainKeyboard(one_time_keyboard=True)

    await message.answer('It`s your rubrics', reply_markup=keyboard)


@dp.message_handler(text=LinksAndRubricsMainKeyboard.text_for_button_to_add_rubric)
async def add_rubric(message: types.Message):
    """ Add a new rubric """

    # ------------------------------------------------------
    # add rubric
    # ------------------------------------------------------
    keyboard = LinksAndRubricsMainKeyboard(one_time_keyboard=True)

    await message.answer('Adding not implemented', reply_markup=keyboard)


@dp.message_handler(text=LinksAndRubricsMainKeyboard.text_for_button_to_delete_rubric)
async def delete_rubric(message: types.Message):
    """ Delete the rubric """

    # ------------------------------------------------------
    # delete rubric
    # ------------------------------------------------------
    keyboard = LinksAndRubricsMainKeyboard(one_time_keyboard=True)

    await message.answer('Deleting not implemented', reply_markup=keyboard)
