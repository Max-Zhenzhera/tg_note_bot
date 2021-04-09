"""
Contains user rubrics handlers.
"""

import logging

from aiogram import types
from aiogram.dispatcher import FSMContext

from ...db.validation import (
    ValidationError,
    RubricValidator,
    get_formatted_error_message
)
from ...states import (
    RubricAddingStatesGroup,
    RubricDeletingStatesGroup
)
# dp loading ^^^^^^^^^^^
from ...loader import dp
# ^^^^^^^^^^^^^^^^^^^^^^
from ...keyboards.reply import LinksAndRubricsMainKeyboard


logger = logging.getLogger(__name__)


# See rubrics ----------------------------------------------------------------------------------------------------------
@dp.message_handler(text=LinksAndRubricsMainKeyboard.text_for_button_to_see_rubrics)
async def see_rubrics(message: types.Message):
    """ Answer with list of the rubrics"""

    # ------------------------------------------------------
    # fetch rubrics
    # ------------------------------------------------------
    keyboard = LinksAndRubricsMainKeyboard(one_time_keyboard=True)

    await message.answer('It`s your rubrics', reply_markup=keyboard)
# ----------------------------------------------------------------------------------------------------------------------


# Add rubric -----------------------------------------------------------------------------------------------------------
@dp.message_handler(text=LinksAndRubricsMainKeyboard.text_for_button_to_add_rubric)
async def add_rubric__catch_message(message: types.Message):
    """ Trigger on rubric adding message """
    await message.answer('Input rubric name [required].')

    await RubricAddingStatesGroup.handling_of_rubric_name.set()


@dp.message_handler(state=RubricAddingStatesGroup.handling_of_rubric_name)
async def add_rubric__handle_rubric_name(message: types.Message, state: FSMContext):
    """ Handle rubric name """
    rubric_name = message.text

    try:
        rubric_name = RubricValidator().validate_rubric_name(rubric_name)
    except ValidationError as error:
        await message.answer(get_formatted_error_message(error))

        return
    else:
        async with state.proxy() as data:
            data['rubric_name'] = rubric_name

        await message.answer('Rubric name has been accepted.')
        await message.answer('Input rubric description [optional].')

        await RubricAddingStatesGroup.next()


@dp.message_handler(state=RubricAddingStatesGroup.handling_of_rubric_description)
async def add_rubric__handle_rubric_description(message: types.Message, state: FSMContext):
    """ Handle rubric name. Last state -> adding to db. """
    rubric_description = message.text

    try:
        rubric_description = RubricValidator().validate_rubric_description(rubric_description)
    except ValidationError as error:
        await message.answer(get_formatted_error_message(error))

        return
    else:
        async with state.proxy() as data:
            rubric_name = data['rubric_name']

        await message.answer('Rubric description has been accepted.')

        keyboard = LinksAndRubricsMainKeyboard(one_time_keyboard=True)
        await message.answer(f'Rubric name: {rubric_name}; rubric desd: {rubric_description}', reply_markup=keyboard)

        await state.finish()

# ----------------------------------------------------------------------------------------------------------------------


@dp.message_handler(text=LinksAndRubricsMainKeyboard.text_for_button_to_delete_rubric)
async def delete_rubric(message: types.Message):
    """ Delete the rubric """

    # ------------------------------------------------------
    # delete rubric
    # ------------------------------------------------------
    keyboard = LinksAndRubricsMainKeyboard(one_time_keyboard=True)

    await message.answer('Deleting not implemented', reply_markup=keyboard)
