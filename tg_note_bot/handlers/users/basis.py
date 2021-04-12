"""
Contains basis user handlers.

.. async:: command_start(message: types.Message)
    Answer on start command and add user to db
.. async:: command_help(message: types.Message)
    Answer on help command
.. async:: command_cancel(message: types.Message, state: FSMContext)
    Cancel current action - reset state
"""

import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import (
    CommandHelp,
    CommandStart
)
from aiogram.utils import markdown as md

from ... import db
from ...db import UserAlreadyInDbError
from ...db.models import User
from ...keyboards.reply import LinksAndRubricsMainReplyKeyboard
from ...loader import (
    dp,
    async_db_sessionmaker
)

logger = logging.getLogger(__name__)


@dp.message_handler(CommandStart())
async def command_start(message: types.Message):
    """ Answer on start command and add user to db """
    user_data = message.from_user
    user_tg_id = user_data.id
    user = User(id=user_tg_id)

    try:
        async with async_db_sessionmaker() as session:
            await db.add_user(session, user)
    except UserAlreadyInDbError:
        logger.debug(f'User with <id={user_tg_id}> has already been in the database.')

        text = f'Hello, friend! Do you wanna add something new ? '
    else:
        logger.debug(f'User with <id={user_tg_id}> has been added in the database.')
        logger.info(f'New user: {user_data.id} | {user_data.username} | {user_data.full_name}')

        text = md.text(
            f'Hello, {md.hbold(message.from_user.username)}! ',
            f'I`m your small {md.hitalic("links saver helper")}:) Explore more with the | /help | command! '
            f'NOTE (BOT`S NOW IN DEVELOPMENT - HE DOESN`T WORK NOW!)'
        )

    keyboard = LinksAndRubricsMainReplyKeyboard(one_time_keyboard=True)
    await message.answer(text, reply_markup=keyboard)


@dp.message_handler(CommandHelp())
async def command_help(message: types.Message):
    """ Answer on help command """
    text = 'Not implemented'
    await message.answer("\n".join(text))


@dp.message_handler(commands=['cancel'], state='*')
async def command_cancel(message: types.Message, state: FSMContext):
    """ Cancel current action - reset state """
    await state.finish()

    keyboard = LinksAndRubricsMainReplyKeyboard(one_time_keyboard=True)
    await message.answer('The current action has canceled!', reply_markup=keyboard)
