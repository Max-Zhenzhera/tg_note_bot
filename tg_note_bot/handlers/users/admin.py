"""
Contains handler for admins.

.. async:: admin_help_command(message: types.Message) -> None
.. async:: user_count(message: types.Message) -> None
.. async:: how_all_bugs(message: types.Message) -> None
.. async:: show_unwatched_bugs(message: types.Message) -> None
"""

import logging

from aiogram import types
from aiogram.dispatcher.filters import IDFilter
from aiogram.utils import markdown as md

from ... import db
from ...loader import (
    dp,
    async_db_sessionmaker
)
from ...settings import ADMINS


logger = logging.getLogger(__name__)


@dp.message_handler(IDFilter(ADMINS), commands=['admin_commands'])
async def admin_help_command(message: types.Message) -> None:
    """ Show admin commands """
    text = md.text(
        *[
            f'{md.hbold(command)}: {text}'
            for command, text in [
                ('/admin_commands', 'show this message;'),
                ('/admin_user_count', 'fetch users quantity;'),
                ('/admin_all_bugs', 'fetch all bugs;'),
                ('/admin_unwatched_bugs', 'fetch unwatched bugs.'),
            ]
        ],
        sep='\n'
    )
    await message.answer(text)


@dp.message_handler(IDFilter(ADMINS), commands=['admin_user_count'])
async def user_count(message: types.Message) -> None:
    """ Show user count """

    async with async_db_sessionmaker() as session:
        users_quantity = await db.count_bot_users(session)

    text = md.text(
        f'Admin {message.from_user.username},',
        md.hbold(users_quantity),
        'users have tried to interact with bot.'
    )
    await message.answer(text)


@dp.message_handler(IDFilter(ADMINS), commands=['admin_all_bugs'])
async def show_all_bugs(message: types.Message) -> None:
    """ Show all bugs """

    async with async_db_sessionmaker() as session:
        bugs = await db.fetch_all_bugs(session)

    text = md.text(
        md.hbold('List of all bugs:'),
        *[
            bug.tg_repr
            for bug in bugs
        ],
        sep='\n' + '➖' * 10 + '\n'
    )
    await message.answer(text)

    async with async_db_sessionmaker() as session:
        await db.mark_all_bugs_as_watched(session)


@dp.message_handler(IDFilter(ADMINS), commands=['admin_unwatched_bugs'])
async def show_unwatched_bugs(message: types.Message) -> None:
    """ Show unwatched bugs """

    async with async_db_sessionmaker() as session:
        bugs = await db.fetch_all_unwatched_bugs(session)

    text = md.text(
        md.hbold('List of unwatched bugs:'),
        *[
            bug.tg_repr
            for bug in bugs
        ],
        sep='\n' + '➖' * 10 + '\n'
    )
    await message.answer(text)

    async with async_db_sessionmaker() as session:
        await db.mark_all_bugs_as_watched(session)
