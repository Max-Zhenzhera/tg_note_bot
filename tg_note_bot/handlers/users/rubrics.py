"""
Contains user rubrics handlers.

.. async:: see_rubrics(message: types.Message) -> None

.. async:: add_rubric__catch_message(message: types.Message) -> None
.. async:: add_rubric__handle_rubric_name(message: types.Message, state: FSMContext) -> None
.. async:: add_rubric__handle_empty_rubric_description(message: types.Message, state: FSMContext) -> None
.. async:: add_rubric__handle_rubric_description(message: types.Message, state: FSMContext) -> None
.. async:: add_rubric__finish(message: types.Message, state: FSMContext, rubric_data: dict) -> None

.. async:: delete_rubric__catch_message(message: types.Message) -> None
.. async:: delete_rubric__handle_rubric_data(call: types.CallbackQuery, callback_data: dict, state: FSMContext) -> None
.. async:: delete_rubric__handle_rubric_links_decision_to_set_non_rubric(message: types.Message, state: FSMContext
        ) -> None
.. async:: delete_rubric__handle_rubric_links_decision_to_delete(message: types.Message, state: FSMContext) -> None
.. async:: delete_rubric__handle_rubric_links_decision_to_move(message: types.Message, state: FSMContext) -> None
.. async:: delete_rubric__handle_new_rubric_for_links_moving(call: types.CallbackQuery, callback_data: dict,
        state: FSMContext) -> None
"""

import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils import markdown as md

from ... import db
from ...db import (
    get_formatted_error_message,
    ValidationError,
    RubricValidator
)
from ...db.models import Rubric
from ...keyboards.inline import (
    RUBRIC_CB,
    RubricListInlineKeyboard
)
from ...keyboards.reply import (
    EmptyValueReplyKeyboard,
    LinksAndRubricsMainReplyKeyboard,
    DecisionAboutRubricLinksOnDeletingReplyKeyboard
)
from ...loader import (
    dp,
    async_db_sessionmaker
)
from ...settings import EMPTY_VALUE
from ...states import (
    RubricAddingStatesGroup,
    RubricDeletingStatesGroup
)


logger = logging.getLogger(__name__)


# callback constants for filtering  - - - - - - - - - - - -
RUBRIC_CB_ACTION_FOR_RUBRIC_DELETING = 'RUBRIC_DELETING'
RUBRIC_CB_ACTION_FOR_LINKS_MOVING = 'LINKS_MOVING'
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


# See rubrics ----------------------------------------------------------------------------------------------------------
@dp.message_handler(text=LinksAndRubricsMainReplyKeyboard.text_for_button_to_see_rubrics)
async def see_rubrics(message: types.Message) -> None:
    """ Answer with list of the rubrics"""
    user_id = message.from_user.id

    async with async_db_sessionmaker() as session:
        rubrics = await db.fetch_all_rubrics(session, user_id)

    if rubrics:
        text = md.text(
            'It`s a list of your rubrics:',
            *[
                '{list_divider} {tg_repr}'.format(list_divider='\t * ', tg_repr=rubric.full_tg_repr)
                for rubric in rubrics
            ],
            sep='\n'
        )
    else:
        text = 'List of the rubrics is empty!'

    keyboard = LinksAndRubricsMainReplyKeyboard(one_time_keyboard=True)
    await message.answer(text, reply_markup=keyboard)
# ----------------------------------------------------------------------------------------------------------------------


# Add rubric -----------------------------------------------------------------------------------------------------------
async def add_rubric__finish(message: types.Message, state: FSMContext, rubric_data: dict) -> None:
    """
    Finish step of rubric adding: to add rubric to db, to finish state.

    :param message: to answer
    :type message: types.Message
    :param state: to finish
    :type state: FSMContext
    :param rubric_data: rubric data that will be passed in `Rubric` model instance
    :type rubric_data: dict

    :return: None
    :rtype: None
    """

    user_id = message.from_user.id

    rubric = Rubric(**rubric_data, user_id=user_id)

    async with async_db_sessionmaker() as session:
        await db.add_rubric(session, rubric)

    text = md.hbold('The new rubric has been added!')
    keyboard = LinksAndRubricsMainReplyKeyboard(one_time_keyboard=True)
    await message.answer(text, reply_markup=keyboard)

    await state.finish()


@dp.message_handler(text=LinksAndRubricsMainReplyKeyboard.text_for_button_to_add_rubric)
async def add_rubric__catch_message(message: types.Message) -> None:
    """ Trigger on rubric adding message. Ask to input rubric name """
    text = 'Input rubric name [required and unique].'
    keyboard = types.ReplyKeyboardRemove()
    await message.answer(text, reply_markup=keyboard)

    await RubricAddingStatesGroup.handling_of_rubric_name.set()


@dp.message_handler(state=RubricAddingStatesGroup.handling_of_rubric_name)
async def add_rubric__handle_rubric_name(message: types.Message, state: FSMContext) -> None:
    """ Handle rubric name. Ask to input rubric description """
    rubric_name = message.text

    try:
        rubric_name = RubricValidator().validate_rubric_name(rubric_name)
    except ValidationError as error:
        await message.answer(get_formatted_error_message(error))
    else:
        user_id = message.from_user.id

        async with async_db_sessionmaker() as session:
            rubric_name_is_unique = await db.does_rubric_have_unique_name(session, user_id, rubric_name)

        if rubric_name_is_unique:
            async with state.proxy() as data:
                data['name'] = rubric_name
            await message.answer('Rubric name has been accepted.')

            text = 'Input rubric description [optional].'
            keyboard = EmptyValueReplyKeyboard(one_time_keyboard=True, resize_keyboard=True)
            await message.answer(text, reply_markup=keyboard)

            await RubricAddingStatesGroup.next()
        else:
            text = (
                f'Oops... Sorry, but {md.hbold("you`ve entered non-unique rubric name")}! '
                f'Please, try to create rubric again and be aware with unique name!'
            )
            await message.answer(text)


@dp.message_handler(text=EMPTY_VALUE, state=RubricAddingStatesGroup.handling_of_rubric_description)
async def add_rubric__handle_empty_rubric_description(message: types.Message, state: FSMContext) -> None:
    """ Handle empty rubric description. Last state -> add rubric to db. """
    async with state.proxy() as data:
        data['description'] = None
    await message.answer('Empty value has been accepted as rubric description.')

    await add_rubric__finish(message, state, data)


@dp.message_handler(state=RubricAddingStatesGroup.handling_of_rubric_description)
async def add_rubric__handle_rubric_description(message: types.Message, state: FSMContext) -> None:
    """ Handle rubric description. Last state -> add rubric to db. """
    rubric_description = message.text

    try:
        rubric_description = RubricValidator().validate_rubric_description(rubric_description)
    except ValidationError as error:
        keyboard = EmptyValueReplyKeyboard(one_time_keyboard=True, resize_keyboard=True)
        await message.answer(get_formatted_error_message(error), reply_markup=keyboard)
    else:
        async with state.proxy() as data:
            data['description'] = rubric_description
        await message.answer('Rubric description has been accepted.')

        await add_rubric__finish(message, state, data)
# ----------------------------------------------------------------------------------------------------------------------


# Delete rubric --------------------------------------------------------------------------------------------------------
@dp.message_handler(text=LinksAndRubricsMainReplyKeyboard.text_for_button_to_delete_rubric)
async def delete_rubric__catch_message(message: types.Message) -> None:
    """ Trigger on rubric deleting message. Ask to choose one of the rubric list """
    user_id = message.from_user.id

    async with async_db_sessionmaker() as session:
        rubrics = await db.fetch_all_rubrics(session, user_id)

    if rubrics:
        text = 'Please, choose one from the list below:'
        keyboard = RubricListInlineKeyboard(rubrics, action=RUBRIC_CB_ACTION_FOR_RUBRIC_DELETING, row_width=1)

        await RubricDeletingStatesGroup.handling_of_rubric_data.set()
    else:
        text = 'You don`t have any rubrics!'
        keyboard = LinksAndRubricsMainReplyKeyboard(one_time_keyboard=True)

    await message.answer(text, reply_markup=keyboard)


@dp.callback_query_handler(
    RUBRIC_CB.filter(action=RUBRIC_CB_ACTION_FOR_RUBRIC_DELETING),
    state=RubricDeletingStatesGroup.handling_of_rubric_data
)
async def delete_rubric__handle_rubric_data(call: types.CallbackQuery, callback_data: dict, state: FSMContext) -> None:
    """ Handle rubric data. Ask to make a decision about rubric links """
    user_id = call.from_user.id

    rubric_id = callback_data['id']
    rubric_name = callback_data['name']

    async with async_db_sessionmaker() as session:
        does_have_rubric_any_links = await db.does_rubric_have_any_links(session, rubric_id)

    if does_have_rubric_any_links:
        async with state.proxy() as data:
            data['id'] = rubric_id
            data['name'] = rubric_name

        text = 'What do you prefer to do with the links that related with the current rubric?'

        async with async_db_sessionmaker() as session:
            user_rubrics_quantity = await db.count_user_rubrics(session, user_id)

        if user_rubrics_quantity == 1:
            keyboard = DecisionAboutRubricLinksOnDeletingReplyKeyboard(
                does_user_have_other_rubrics=False, one_time_keyboard=True, resize_keyboard=True
            )
        else:
            keyboard = DecisionAboutRubricLinksOnDeletingReplyKeyboard(one_time_keyboard=True, resize_keyboard=True)

        await RubricDeletingStatesGroup.next()
    else:
        text = f'Rubric ({md.hbold(rubric_name)}) has been deleted!'
        keyboard = LinksAndRubricsMainReplyKeyboard(one_time_keyboard=True)

        async with async_db_sessionmaker() as session:
            await db.delete_rubric(session, rubric_id)

        await state.finish()

    await call.message.answer(text, reply_markup=keyboard)

    await call.answer()


@dp.message_handler(
    text=DecisionAboutRubricLinksOnDeletingReplyKeyboard.text_for_button_to_set_none_rubric_for_links,
    state=RubricDeletingStatesGroup.handling_of_decision_about_rubric_links
)
async def delete_rubric__handle_rubric_links_decision_to_set_non_rubric(message: types.Message, state: FSMContext
                                                                        ) -> None:
    """ Handle decision. Delete rubric [by default rubric deleting does not remove related links] """
    async with state.proxy() as data:
        rubric_id = data['id']
        rubric_name = data['name']

    async with async_db_sessionmaker() as session:
        await db.delete_rubric(session, rubric_id)

    text = f'Rubric ({md.hbold(rubric_name)}) has been deleted!'
    keyboard = LinksAndRubricsMainReplyKeyboard(one_time_keyboard=True)
    await message.answer(text, reply_markup=keyboard)


@dp.message_handler(
    text=DecisionAboutRubricLinksOnDeletingReplyKeyboard.text_for_button_to_delete_links,
    state=RubricDeletingStatesGroup.handling_of_decision_about_rubric_links
)
async def delete_rubric__handle_rubric_links_decision_to_delete(message: types.Message, state: FSMContext) -> None:
    """ Handle decision. Delete rubric and related links """
    async with state.proxy() as data:
        rubric_id = data['id']
        rubric_name = data['name']

    async with async_db_sessionmaker() as session:
        await db.delete_rubric(session, rubric_id, delete_links=True)

    text = f'Rubric ({md.hbold(rubric_name)}) has been deleted!'
    keyboard = LinksAndRubricsMainReplyKeyboard(one_time_keyboard=True)
    await message.answer(text, reply_markup=keyboard)


@dp.message_handler(
    text=DecisionAboutRubricLinksOnDeletingReplyKeyboard.text_for_button_to_delete_links,
    state=RubricDeletingStatesGroup.handling_of_decision_about_rubric_links
)
async def delete_rubric__handle_rubric_links_decision_to_move(message: types.Message, state: FSMContext) -> None:
    """ Handle decision. Ask to which rubric move related links """
    user_id = message.from_user.id

    async with state.proxy() as data:
        rubric_id = data['id']
        rubric_name = data['name']

    async with async_db_sessionmaker() as session:
        rubrics = await db.fetch_all_rubrics(session, user_id)

    text = f'Choose on of the list below: [all links related with {md.hbold(rubric_name)} will be moved in ...]'
    keyboard = RubricListInlineKeyboard(
        rubrics, action=RUBRIC_CB_ACTION_FOR_LINKS_MOVING, row_width=1, except_rubrics_with_id={rubric_id, }
    )
    await message.answer(text, reply_markup=keyboard)

    await RubricDeletingStatesGroup.next()


@dp.callback_query_handler(
    RUBRIC_CB.filter(action=RUBRIC_CB_ACTION_FOR_LINKS_MOVING),
    state=RubricDeletingStatesGroup.handling_of_new_rubric_to_move_links_into
)
async def delete_rubric__handle_new_rubric_for_links_moving(call: types.CallbackQuery, callback_data: dict,
                                                            state: FSMContext
                                                            ) -> None:
    """ Handle new rubric data. Delete rubric and move related links in another rubric """
    user_id = call.from_user.id

    async with state.proxy() as data:
        rubric_id = data['id']
        rubric_name = data['name']

    # new -> rubric for links migrating
    new_rubric_id = callback_data['id']
    new_rubric_name = callback_data['name']

    async with async_db_sessionmaker() as session:
        await db.migrate_links_in_another_rubric(session, user_id, rubric_id, new_rubric_id)
        await db.delete_rubric(session, rubric_id)

    text = (
        f'Links related with the {md.hbold(rubric_name)} rubric '
        f'have migrated in the {md.hbold(new_rubric_name)} rubric!'
    )
    keyboard = LinksAndRubricsMainReplyKeyboard(one_time_keyboard=True)
    await call.message.answer(text, reply_markup=keyboard)

    await state.finish()

    await call.answer()
# ----------------------------------------------------------------------------------------------------------------------
