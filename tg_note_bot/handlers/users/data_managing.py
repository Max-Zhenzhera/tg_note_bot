"""
Contains handlers for serious deleting.

.. async:: manage_deleting__catch_message(message: types.Message) -> None
.. async:: manage_deleting__comeback(message: types.Message, state: FSMContext) -> None
.. async:: manage_deleting__ask_user_confirmation(message: types.Message, state: FSMContext,
        db_function_key: str, message_if_confirmed: str) -> None

.. async:: manage_deleting__delete_all_links(message: types.Message, state: FSMContext) -> None
.. async:: manage_deleting__delete_all_rubrics(message: types.Message, state: FSMContext) -> None
.. async:: manage_deleting__delete_all_rubric_links(message: types.Message, state: FSMContext) -> None
.. async:: manage_deleting__delete_all_non_rubric_links(message: types.Message, state: FSMContext) -> None
.. async:: manage_deleting__delete_all_data(message: types.Message, state: FSMContext) -> None

.. async:: manage_deleting__execute_after_confirmation(message: types.Message, state: FSMContext) -> None
.. async:: manage_deleting__cancel_after_refusal(message: types.Message, state: FSMContext) -> None
.. async:: manage_deleting__redirect_after_main_menu_choice(message: types.Message, state: FSMContext) -> None
"""

import logging

from aiogram import types
from aiogram.dispatcher import FSMContext

from ... import db
from ...keyboards.reply import (
    YesOrNotReplyKeyboard,
    LinksAndRubricsMainReplyKeyboard,
    ManageSeriousDeletingReplyKeyboard
)
from ...loader import (
    dp,
    async_db_sessionmaker
)
from ...states import ManageSeriousDeletingStatesGroup


logger = logging.getLogger(__name__)


# Used Redis FSM storage - values must be JSON-serializable ------------------------------------------------------------
KEY_DELETE_ALL_LINKS = 'DELETE_ALL_LINKS'
KEY_DELETE_ALL_RUBRICS = 'DELETE_ALL_RUBRICS'
KEY_DELETE_ALL_RUBRIC_LINKS = 'DELETE_ALL_RUBRIC_LINKS'
KEY_DELETE_ALL_NON_RUBRIC_LINKS = 'DELETE_ALL_NON_RUBRIC_LINKS'
KEY_DELETE_ALL_USER_DATA = 'DELETE_ALL_USER_DATA'

# function_key: function | proxy mapper
DB_DELETE_FUNCTIONS_MAPPER = {
    KEY_DELETE_ALL_LINKS: db.delete_all_links_by_user,
    KEY_DELETE_ALL_RUBRICS: db.delete_all_rubrics,
    KEY_DELETE_ALL_RUBRIC_LINKS: db.delete_all_rubric_links_by_user,
    KEY_DELETE_ALL_NON_RUBRIC_LINKS: db.delete_all_non_rubric_links_by_user,
    KEY_DELETE_ALL_USER_DATA: db.delete_all_user_data
}
# ----------------------------------------------------------------------------------------------------------------------


@dp.message_handler(text=LinksAndRubricsMainReplyKeyboard.text_for_button_to_manage_serious_deleting)
async def manage_deleting__catch_message(message: types.Message) -> None:
    """ Trigger on delete managing message. Ask for choice """
    text = '☢️ Please, be careful! It`s a very serious section! ☢️'
    keyboard = ManageSeriousDeletingReplyKeyboard(one_time_keyboard=True)
    await message.answer(text, reply_markup=keyboard)

    await ManageSeriousDeletingStatesGroup.handling_of_delete_choice.set()


@dp.message_handler(
    text=ManageSeriousDeletingReplyKeyboard.text_for_button_to_comeback,
    state=ManageSeriousDeletingStatesGroup.handling_of_delete_choice
)
async def manage_deleting__comeback(message: types.Message, state: FSMContext) -> None:
    """ Trigger on delete managing message. Ask for choice """
    text = '✅ Comeback main menu!'
    keyboard = LinksAndRubricsMainReplyKeyboard(one_time_keyboard=True)
    await message.answer(text, reply_markup=keyboard)

    await state.finish()


async def manage_deleting__ask_user_confirmation(message: types.Message, state: FSMContext,
                                                 db_function_key: str, message_if_confirmed: str
                                                 ) -> None:
    """
    Ask user for confirmation and set in state delete data.

    :param message: to answer
    :type message: types.Message
    :param state: to set data
    :type state: FSMContext
    :param db_function_key: state data
    :type db_function_key: str
    :param message_if_confirmed: state data
    :type message_if_confirmed: str

    :return: None
    :rtype: None
    """

    async with state.proxy() as data:
        data['db_function_key'] = db_function_key
        data['message_if_confirmed'] = message_if_confirmed

    text = '❔ Are you sure ❔'
    keyboard = YesOrNotReplyKeyboard(one_time_keyboard=True, resize_keyboard=True)
    await message.answer(text, reply_markup=keyboard)

    await ManageSeriousDeletingStatesGroup.next()


@dp.message_handler(
    text=ManageSeriousDeletingReplyKeyboard.text_for_button_to_delete_all_links,
    state=ManageSeriousDeletingStatesGroup.handling_of_delete_choice
)
async def manage_deleting__delete_all_links(message: types.Message, state: FSMContext) -> None:
    """ Trigger on delete all links message. Ask to confirm """
    db_function_key = KEY_DELETE_ALL_LINKS
    message_if_confirmed = '✅ All links have been deleted!'

    await manage_deleting__ask_user_confirmation(message, state, db_function_key, message_if_confirmed)


@dp.message_handler(
    text=ManageSeriousDeletingReplyKeyboard.text_for_button_to_delete_all_rubrics,
    state=ManageSeriousDeletingStatesGroup.handling_of_delete_choice
)
async def manage_deleting__delete_all_rubrics(message: types.Message, state: FSMContext) -> None:
    """ Trigger on delete all rubrics message. Ask to confirm """
    db_function_key = KEY_DELETE_ALL_RUBRICS
    message_if_confirmed = '✅ All rubrics have been deleted! All rubric links have migrated in non-rubric!'

    await manage_deleting__ask_user_confirmation(message, state, db_function_key, message_if_confirmed)


@dp.message_handler(
    text=ManageSeriousDeletingReplyKeyboard.text_for_button_to_delete_all_rubric_links,
    state=ManageSeriousDeletingStatesGroup.handling_of_delete_choice
)
async def manage_deleting__delete_all_rubric_links(message: types.Message, state: FSMContext) -> None:
    """ Trigger on delete all rubric links message. Ask to confirm """
    db_function_key = KEY_DELETE_ALL_RUBRIC_LINKS
    message_if_confirmed = '✅ All rubric links have been deleted! All rubrics are empty now!'

    await manage_deleting__ask_user_confirmation(message, state, db_function_key, message_if_confirmed)


@dp.message_handler(
    text=ManageSeriousDeletingReplyKeyboard.text_for_button_to_delete_all_non_rubric_links,
    state=ManageSeriousDeletingStatesGroup.handling_of_delete_choice
)
async def manage_deleting__delete_all_non_rubric_links(message: types.Message, state: FSMContext) -> None:
    """ Trigger on delete all non rubric links message. Ask to confirm """
    db_function_key = KEY_DELETE_ALL_NON_RUBRIC_LINKS
    message_if_confirmed = '✅ All non rubric links (🖤) have been deleted!'

    await manage_deleting__ask_user_confirmation(message, state, db_function_key, message_if_confirmed)


@dp.message_handler(
    text=ManageSeriousDeletingReplyKeyboard.text_for_button_to_delete_all,
    state=ManageSeriousDeletingStatesGroup.handling_of_delete_choice
)
async def manage_deleting__delete_all_data(message: types.Message, state: FSMContext) -> None:
    """ Trigger on delete all non rubric links message. Ask to confirm """
    db_function_key = KEY_DELETE_ALL_USER_DATA
    message_if_confirmed = '✅ All data has been deleted! No one link and rubric have left! (🕳)'

    await manage_deleting__ask_user_confirmation(message, state, db_function_key, message_if_confirmed)


@dp.message_handler(
    text=YesOrNotReplyKeyboard.text_for_button_with_yes,
    state=ManageSeriousDeletingStatesGroup.handling_of_user_confirmation
)
async def manage_deleting__execute_after_confirmation(message: types.Message, state: FSMContext) -> None:
    """ Handle user confirmation [yes]. Delete entities by function passed in state data """
    user_id = message.from_user.id

    async with state.proxy() as data:
        db_function = DB_DELETE_FUNCTIONS_MAPPER[data['db_function_key']]
        text = data['message_if_confirmed']

    async with async_db_sessionmaker() as session:
        await db_function(session, user_id)

    keyboard = ManageSeriousDeletingReplyKeyboard(one_time_keyboard=True)
    await message.answer(text, reply_markup=keyboard)

    await state.finish()
    await ManageSeriousDeletingStatesGroup.handling_of_delete_choice.set()


@dp.message_handler(
    text=YesOrNotReplyKeyboard.text_for_button_with_not,
    state=ManageSeriousDeletingStatesGroup.handling_of_user_confirmation
)
async def manage_deleting__cancel_after_refusal(message: types.Message, state: FSMContext) -> None:
    """ Handle user confirmation [not]. Cancel deleting """
    text = '❌ Deleting cancelled!'
    keyboard = ManageSeriousDeletingReplyKeyboard(one_time_keyboard=True)
    await message.answer(text, reply_markup=keyboard)

    await state.finish()
    await ManageSeriousDeletingStatesGroup.handling_of_delete_choice.set()


@dp.message_handler(
    text=YesOrNotReplyKeyboard.text_for_button_to_comeback_main_menu,
    state=ManageSeriousDeletingStatesGroup.handling_of_user_confirmation
)
async def manage_deleting__redirect_after_main_menu_choice(message: types.Message, state: FSMContext) -> None:
    """ Handle user confirmation [main menu]. Forward to main menu """
    text = '❌ Deleting cancelled! | ✅ Comeback main menu!'
    keyboard = LinksAndRubricsMainReplyKeyboard(one_time_keyboard=True)
    await message.answer(text, reply_markup=keyboard)

    await state.finish()
