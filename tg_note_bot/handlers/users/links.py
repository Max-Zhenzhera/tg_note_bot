"""
Contains user links handlers.
"""

import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils import markdown as md

from ...loader import (
    dp,
    async_db_sessionmaker
)
from ...states import LinkAddingStatesGroup
from ...db.validation import (
    ValidationError,
    LinkValidator,
    get_formatted_error_message
)
from ...db.models import Link, Rubric
from ...keyboards.reply import (
    EmptyValueReplyKeyboard,
    LinksAndRubricsMainReplyKeyboard
)
from ...keyboards.inline import (
    RUBRIC_CB,
    RubricListInlineKeyboard
)
from ...settings import EMPTY_VALUE


logger = logging.getLogger(__name__)


# callback constants for filtering  - - - - - - - - - - - -
RUBRIC_CB_ACTION_FOR_LINK_ADDING = 'RUBRIC_DELETING'
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


@dp.message_handler(text=LinksAndRubricsMainReplyKeyboard.text_for_button_to_see_links)
async def see_links(message: types.Message):
    """ Answer with list of the links"""
    session: AsyncSession
    async with async_db_sessionmaker(Link) as session:
        stmt_to_fetch_links_with_rubric = select(Rubric).options(selectinload(Rubric.links)).order_by(Rubric.name)
        stmt_to_fetch_links_without_rubric = select(Link).where(Link.rubric_id is None)
        result_with_links_with_rubric = await session.execute(stmt_to_fetch_links_with_rubric)
        result_with_links_without_rubric = await session.execute(stmt_to_fetch_links_without_rubric)

    keyboard = LinksAndRubricsMainReplyKeyboard(one_time_keyboard=True)

    await message.answer('It`s your links', reply_markup=keyboard)


@dp.message_handler(text=LinksAndRubricsMainReplyKeyboard.text_for_button_to_see_links_by_rubric)
async def see_links_by_rubrics(message: types.Message):
    """ Answer with list of the links sorted by rubric """

    # ------------------------------------------------------
    # fetch links by rubric
    # ------------------------------------------------------
    keyboard = LinksAndRubricsMainReplyKeyboard(one_time_keyboard=True)

    await message.answer('It`s your links by rubric', reply_markup=keyboard)


# Add link -----------------------------------------------------------------------------------------------------------
@dp.message_handler(text=LinksAndRubricsMainReplyKeyboard.text_for_button_to_add_link)
async def add_link__catch_message(message: types.Message):
    """ Trigger on link adding message. Ask to input link url """
    await message.answer('Input url [required].', reply_markup=types.ReplyKeyboardRemove())

    await LinkAddingStatesGroup.handling_of_link_url.set()


@dp.message_handler(state=LinkAddingStatesGroup.handling_of_link_url)
async def add_link__handle_link_url(message: types.Message, state: FSMContext):
    """ Handle link url. Ask to input link description """
    link_url = message.text

    try:
        link_url = LinkValidator().validate_link_url(link_url)
    except ValidationError as error:
        await message.answer(get_formatted_error_message(error))

        return
    else:
        async with state.proxy() as data:
            data['user_id'] = message.from_user.id
            data['url'] = link_url

        await message.answer('Link url has been accepted.')

        keyboard = EmptyValueReplyKeyboard(one_time_keyboard=True, resize_keyboard=True)

        await message.answer('Input link description [optional].', reply_markup=keyboard)

        await LinkAddingStatesGroup.next()


@dp.message_handler(text=EMPTY_VALUE, state=LinkAddingStatesGroup.handling_of_link_description)
async def add_link__handle_empty_link_description(message: types.Message, state: FSMContext):
    """ Handle link description. Ask to choose rubric """
    await message.answer('Empty value has been accepted as link description.')

    async with state.proxy() as data:
        data['description'] = None

    session: AsyncSession
    async with async_db_sessionmaker() as session:
        stmt = select(Rubric).where(Rubric.user_id == message.from_user.id)
        result = await session.execute(stmt)
    rubrics = list(result.scalars())

    text = 'Choose one of the rubrics [optional]'
    keyboard = RubricListInlineKeyboard(
        rubrics, action=RUBRIC_CB_ACTION_FOR_LINK_ADDING, empty_value_on_the_start=True
    )

    await message.answer(text, reply_markup=keyboard)

    await LinkAddingStatesGroup.next()


@dp.message_handler(state=LinkAddingStatesGroup.handling_of_link_description)
async def add_link__handle_link_description(message: types.Message, state: FSMContext):
    """ Handle link description. Ask to choose rubric """
    message_text = message.text
    if message_text == EMPTY_VALUE:
        link_description = None
    else:
        link_description = message_text

    try:
        link_description = LinkValidator().validate_link_description(link_description)
    except ValidationError as error:
        await message.answer(get_formatted_error_message(error))

        return
    else:
        await message.answer('Link description has been accepted.')

        async with state.proxy() as data:
            data['description'] = link_description

        session: AsyncSession
        async with async_db_sessionmaker() as session:
            stmt = select(Rubric).where(Rubric.user_id == message.from_user.id)
            result = await session.execute(stmt)
        rubrics = list(result.scalars())

        text = 'Choose one of the rubrics [optional]'
        keyboard = RubricListInlineKeyboard(
            rubrics, action=RUBRIC_CB_ACTION_FOR_LINK_ADDING, empty_value_on_the_start=True
        )

        await message.answer(text, reply_markup=keyboard)

        await LinkAddingStatesGroup.next()


@dp.callback_query_handler(RUBRIC_CB.filter(action=RUBRIC_CB_ACTION_FOR_LINK_ADDING), state=LinkAddingStatesGroup.handling_of_link_rubric)
async def add_link__handle_link_rubric(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    """ Handle link rubric. Last state -> adding link to db. """
    data = await state.get_data()
    print(data)
    print(callback_data)
    await call.answer()
# ----------------------------------------------------------------------------------------------------------------------


@dp.message_handler(text=LinksAndRubricsMainReplyKeyboard.text_for_button_to_delete_link)
async def delete_rubric(message: types.Message):
    """ Delete the link """

    # ------------------------------------------------------
    # delete link
    # ------------------------------------------------------
    keyboard = LinksAndRubricsMainReplyKeyboard(one_time_keyboard=True)

    await message.answer('Deleting not implemented', reply_markup=keyboard)
