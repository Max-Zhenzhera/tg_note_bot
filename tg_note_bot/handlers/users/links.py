"""
Contains user links handlers.
"""

import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils import markdown as md

from ... import db
from ...db.models import (
    Link,
    Rubric
)
from ...db.validation import (
    ValidationError,
    LinkValidator,
    get_formatted_error_message
)
from ...keyboards.inline import (
    LINK_CB,
    LinkListInlineKeyboard,
    RUBRIC_CB,
    RubricListInlineKeyboard
)
from ...keyboards.reply import (
    EmptyValueReplyKeyboard,
    LinksAndRubricsMainReplyKeyboard
)
from ...loader import (
    dp,
    async_db_sessionmaker
)
from ...settings import EMPTY_VALUE
from ...states import LinkAddingStatesGroup

logger = logging.getLogger(__name__)


# callback constants for filtering  - - - - - - - - - - - - - - - - - - -
RUBRIC_CB_ACTION_FOR_LINK_ADDING = 'LINK_ADDING'
RUBRIC_CB_ACTION_FOR_LINK_BY_RUBRIC_SELECTING = 'LINK_BY_RUBRIC_SELECTING'
LINK_CB_ACTION_FOR_LINK_DELETING = 'LINK_DELETING'
LINK_CB_ACTION_FOR_LINK_DUMPING = 'LINK_DUMPING'
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


# See all links --------------------------------------------------------------------------------------------------------
@dp.message_handler(text=LinksAndRubricsMainReplyKeyboard.text_for_button_to_see_links)
async def see_links(message: types.Message) -> None:
    """ Answer with list of the links"""
    user_id = message.from_user.id

    async with async_db_sessionmaker() as session:
        rubrics: dict = await db.fetch_all_links(session, user_id, group_by_rubric=True)

    non_rubric_with_loaded_links = Rubric(name='Non-Rubric', links=rubrics.pop(None, []))

    text = md.text(
        '☑️  Links with rubric:',
        *[
            rubric.repr_with_links('👉', rubric_shift='🔘', links=links)
            for rubric, links in rubrics.items()
        ],
        '➖' * 15,
        '☑️  Non-rubric links:',
        non_rubric_with_loaded_links.repr_with_links('👉', rubric_shift='🖤'),
        sep='\n'
    )
    keyboard = LinksAndRubricsMainReplyKeyboard(one_time_keyboard=True)
    await message.answer(text, reply_markup=keyboard, disable_web_page_preview=True)
# ----------------------------------------------------------------------------------------------------------------------


# Dump link ------------------------------------------------------------------------------------------------------------
@dp.message_handler(text=LinksAndRubricsMainReplyKeyboard.text_for_button_to_dump_link)
async def dump_link__catch_message(message: types.Message) -> None:
    """ Trigger om message. Ask to choose link """
    user_id = message.from_user.id

    async with async_db_sessionmaker() as session:
        links = await db.fetch_all_links(session, user_id, with_rubric=True)

    if links:
        text = '❔ Choose one of the list below:'
        keyboard = LinkListInlineKeyboard(links, action=LINK_CB_ACTION_FOR_LINK_DUMPING, row_width=1)
    else:
        text = '🕳 You don`t have any links'
        keyboard = LinksAndRubricsMainReplyKeyboard(one_time_keyboard=True)

    await message.answer(text, reply_markup=keyboard)


@dp.callback_query_handler(LINK_CB.filter(action=LINK_CB_ACTION_FOR_LINK_DUMPING))
async def dump_link__handle_link_data(call: types.CallbackQuery, callback_data: dict) -> None:
    """ Handle link data. Dump link """
    link_id = callback_data['id']

    async with async_db_sessionmaker() as session:
        link = await db.fetch_one_link(session, link_id, with_rubric=True)

    text = md.text(
        f'☑️  {link.full_tg_repr}',
        f'🧭 created at: {link.created_at.isoformat(" ")}',
        sep='\n'
    )
    keyboard = LinksAndRubricsMainReplyKeyboard(one_time_keyboard=True)
    await call.message.answer(text, reply_markup=keyboard)

    await call.answer()
# ----------------------------------------------------------------------------------------------------------------------


# See links by rubric --------------------------------------------------------------------------------------------------
@dp.message_handler(text=LinksAndRubricsMainReplyKeyboard.text_for_button_to_see_links_by_rubric)
async def see_links_by_rubric__catch_message(message: types.Message) -> None:
    """ Trigger om message. Ask to choose rubric """
    user_id = message.from_user.id

    async with async_db_sessionmaker() as session:
        does_user_have_rubrics = await db.count_user_rubrics(session, user_id)

        if does_user_have_rubrics:
            rubrics = await db.fetch_all_rubrics(session, user_id)

            text = '❔ Choose one of the list below:'
            keyboard = RubricListInlineKeyboard(
                rubrics, action=RUBRIC_CB_ACTION_FOR_LINK_BY_RUBRIC_SELECTING, row_width=1
            )
            await message.answer(text, reply_markup=keyboard)
        else:
            await message.answer('🕳 You don`t have any rubric.')


@dp.callback_query_handler(RUBRIC_CB.filter(action=RUBRIC_CB_ACTION_FOR_LINK_BY_RUBRIC_SELECTING))
async def see_links_by_rubric__handle_rubric_data(call: types.CallbackQuery, callback_data: dict) -> None:
    """ Answer with list of the links sorted by rubric """
    rubric_id = callback_data['id']

    async with async_db_sessionmaker() as session:
        rubrics = await db.fetch_one_rubric(session, rubric_id, with_links=True)

    if rubrics.links:
        text = rubrics.repr_with_loaded_links('👉')
    else:
        text = '🕳 Rubric is empty! It`s no one link is related with this rubric.'

    keyboard = LinksAndRubricsMainReplyKeyboard(one_time_keyboard=True)
    await call.message.answer(text, reply_markup=keyboard, disable_web_page_preview=True)

    await call.answer()
# ----------------------------------------------------------------------------------------------------------------------


# Add link -------------------------------------------------------------------------------------------------------------
async def add_link__finish(user_id: int, message: types.Message, state: FSMContext, link_data: dict) -> None:
    """
    Add link to db. Finish state

    :param user_id: for link data required user id
    :type user_id: int
    :param message: to answer
    :type message: types.Message
    :param state: to finish
    :type state: FSMContext
    :param link_data: for link instance creation
    :type link_data: dict

    :return: None
    :rtype: None
    """

    link = Link(**link_data, user_id=user_id)

    async with async_db_sessionmaker() as session:
        await db.add_link(session, link)

    text = md.hbold('✅ The new link has been added!')
    keyboard = LinksAndRubricsMainReplyKeyboard(one_time_keyboard=True)
    await message.answer(text, reply_markup=keyboard)

    await state.finish()


async def add_link__ask_for_rubric(message: types.Message, state: FSMContext) -> None:
    """ Ask for rubric on link adding | used to avoid repeating in handlers below """
    user_id = message.from_user.id

    async with async_db_sessionmaker() as session:
        rubrics = await db.fetch_all_rubrics(session, user_id)

    if rubrics:
        text = '❔ Choose one of the rubrics [🆓 optional]'
        keyboard = RubricListInlineKeyboard(rubrics, action=RUBRIC_CB_ACTION_FOR_LINK_ADDING, row_width=1)
        await message.answer(text, reply_markup=keyboard)

        await LinkAddingStatesGroup.next()
    else:
        text = '💿 You don`t have any rubric to pin link. This link will be added in | 🖤 | non-rubric category!'
        # remove empty value keyboard
        keyboard = types.ReplyKeyboardRemove()
        await message.answer(text, reply_markup=keyboard)

        async with state.proxy() as data:
            data['rubric_id'] = None

        await add_link__finish(user_id, message, state, data)


@dp.message_handler(text=LinksAndRubricsMainReplyKeyboard.text_for_button_to_add_link)
async def add_link__catch_message(message: types.Message) -> None:
    """ Trigger on link adding message. Ask to input link url """
    text = '📝 Input url [❗️ required].'
    keyboard = types.ReplyKeyboardRemove()
    await message.answer(text, reply_markup=keyboard)

    await LinkAddingStatesGroup.handling_of_link_url.set()


@dp.message_handler(state=LinkAddingStatesGroup.handling_of_link_url)
async def add_link__handle_link_url(message: types.Message, state: FSMContext) -> None:
    """ Handle link url. Ask to input link description """
    link_url = message.text

    try:
        link_url = LinkValidator().validate_link_url(link_url)
    except ValidationError as error:
        await message.answer(get_formatted_error_message(error))
    else:
        async with state.proxy() as data:
            data['url'] = link_url
        await message.answer('👌 Link url has been accepted.')

        text = '📝 Input link description [🆓 optional].'
        # `one_time_keyboard` is omitted - it`ll be used few times [for description and rubric]
        keyboard = EmptyValueReplyKeyboard(resize_keyboard=True)
        await message.answer(text, reply_markup=keyboard)

        await LinkAddingStatesGroup.next()


@dp.message_handler(text=EMPTY_VALUE, state=LinkAddingStatesGroup.handling_of_link_description)
async def add_link__handle_empty_link_description(message: types.Message, state: FSMContext) -> None:
    """ Handle empty link description. Ask to choose rubric """
    async with state.proxy() as data:
        data['description'] = None
    await message.answer('👌 Empty value has been accepted as link description.')

    await add_link__ask_for_rubric(message, state)


@dp.message_handler(state=LinkAddingStatesGroup.handling_of_link_description)
async def add_link__handle_link_description(message: types.Message, state: FSMContext) -> None:
    """ Handle link description. Ask to choose rubric """
    link_description = message.text

    try:
        link_description = LinkValidator().validate_link_description(link_description)
    except ValidationError as error:
        await message.answer(get_formatted_error_message(error))
    else:
        async with state.proxy() as data:
            data['description'] = link_description
        await message.answer('👌 Link description has been accepted.')

        await add_link__ask_for_rubric(message, state)


@dp.message_handler(text=EMPTY_VALUE, state=LinkAddingStatesGroup.handling_of_link_rubric)
async def add_link__handle_empty_link_rubric(message: types.Message, state: FSMContext) -> None:
    """ Handle empty link rubric. Last state -> adding link to db. """
    user_id = message.from_user.id

    async with state.proxy() as data:
        data['rubric_id'] = None

    await message.answer('👌 Empty value has been accepted as link rubric.')

    await add_link__finish(user_id, message, state, data)


@dp.callback_query_handler(
    RUBRIC_CB.filter(action=RUBRIC_CB_ACTION_FOR_LINK_ADDING),
    state=LinkAddingStatesGroup.handling_of_link_rubric
)
async def add_link__handle_link_rubric(call: types.CallbackQuery, callback_data: dict, state: FSMContext) -> None:
    """ Handle link rubric. Last state -> adding link to db. """
    user_id = call.from_user.id

    async with state.proxy() as data:
        data['rubric_id'] = callback_data['id']
    await call.message.answer('👌 Link rubric has been accepted.')

    await call.answer()

    await add_link__finish(user_id, call.message, state, data)
# ----------------------------------------------------------------------------------------------------------------------


# Delete link ----------------------------------------------------------------------------------------------------------
@dp.message_handler(text=LinksAndRubricsMainReplyKeyboard.text_for_button_to_delete_link)
async def delete_link__catch_message(message: types.Message) -> None:
    """ Trigger on link deleting message """
    user_id = message.from_user.id

    async with async_db_sessionmaker() as session:
        links = await db.fetch_all_links(session, user_id, with_rubric=True)

    if links:
        text = '❔ Choose one of the list below:'
        keyboard = LinkListInlineKeyboard(links, action=LINK_CB_ACTION_FOR_LINK_DELETING, row_width=1)
    else:
        text = '🕳 You don`t have any links'
        keyboard = LinksAndRubricsMainReplyKeyboard(one_time_keyboard=True)

    await message.answer(text, reply_markup=keyboard)


@dp.callback_query_handler(LINK_CB.filter(action=LINK_CB_ACTION_FOR_LINK_DELETING))
async def delete_link__handle_link_data(call: types.CallbackQuery, callback_data: dict):
    """ Handle link data. Delete link """
    link_id = callback_data['id']

    async with async_db_sessionmaker() as session:
        await db.delete_one_link(session, link_id)

    text = f'✅ Link has been deleted!'
    keyboard = LinksAndRubricsMainReplyKeyboard(one_time_keyboard=True)
    await call.message.answer(text, reply_markup=keyboard, disable_web_page_preview=True)

    await call.answer()
# ----------------------------------------------------------------------------------------------------------------------
