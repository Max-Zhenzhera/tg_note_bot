"""
Contains basis user handlers.

.. async:: command_start(message: types.Message) -> None
    Answer on start command and add user to db
.. async:: command_help(message: types.Message) -> None
    Answer on help command
.. async:: command_cancel(message: types.Message, state: FSMContext) -> None
    Cancel current action - reset state
.. async:: command_bug(message: types.Message) -> None
    Handle bug report from user
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
from ...db import (
    get_formatted_error_message,
    BugValidator,
    ValidationError,
    UserAlreadyInDbError
)
from ...db.models import Bug
from ...db.models import User
from ...keyboards.reply import LinksAndRubricsMainReplyKeyboard
from ...loader import (
    dp,
    async_db_sessionmaker
)
from ...middlewares.throttling import rate_limit
from ...settings import (
    THROTTLING_RATE_LIMIT_IN_SECONDS_FOR_BUG_COMMAND,
    STICKER_SMILE_WITH_GLASSES,
    STICKER_KISSING_FROG
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

        text = f'👋 Hello, friend! Do you wanna add something new ? '
    else:
        logger.debug(f'User with <id={user_tg_id}> has been added in the database.')
        logger.info(
            f'New user: {user_data.id} | {user_data.username} | {user_data.full_name} ({message.date.isoformat(" ")})'
        )

        text = md.text(
            f'🤘 Hello, {md.hbold(message.from_user.username)}! ',
            f'I`m your small {md.hitalic("links saver helper")} 🔗 '
            'Explore more with the | /help | command!',
            md.hunderline('NOTE (BOT`S NOW IN DEVELOPMENT - 🛠 - HE DOESN`T WORK NOW!)'),
            sep='\n'
        )

        await message.answer_sticker(STICKER_SMILE_WITH_GLASSES)

    keyboard = LinksAndRubricsMainReplyKeyboard(one_time_keyboard=True)
    await message.answer(text, reply_markup=keyboard)


@dp.message_handler(CommandHelp())
async def command_help(message: types.Message):
    """ Answer on help command """
    text = md.text(
        md.hbold('Help message:'),
        md.hbold('What can you do with this bot?'),
        'Keep useful links with rubric sorting and do not flood in saved messages.',
        md.hbold('Commands:'),
        '/start : start interaction with bot, invoke main menu;',
        '/cancel : cancel current action, comeback main menu;',
        '/help : show current help message;',
        '/bug : report about bug (use if smth went wrong, might be invoked once in 5 minutes), e.g. /bug bug message.',
        md.hbold('Interaction:'),
        '👀 - watch all entities of,',
        '💾 - save new,',
        '🔎 - inspect by,',
        '🗑 - delete old,',
        '🔥 - manage serious deleting.',
        md.hbold('Meta:'),
        'We have links and rubrics.',
        'Link contains: url [required], description [optional], rubric [optional].',
        'Rubric contains: name [required], description [optional].',
        'Simple actions as 👀, 💾, 🔎, 🗑 do not require any help. They very simple.',
        'One word about 🗑 rubric: on rubric deleting you have to do smth with related links:',
        'delete all related links, move to non-rubric (🖤) category or move in another rubric.',
        '🔥 section has some offers to manage data and should be written here:',
        '🔥 all links - simply delete all links (rubrics won`t be deleted),',
        '🔥 all rubrics - delete all rubrics (related links will be moved in non-rubric category),',
        '🔥 all rubric links - delete all links that have rubric (rubrics won`t be deleted - only related links),',
        '🔥 all non-rubric links - delete all links from (🖤) non-rubric category (links that don`t have rubric),',
        '🔥 all - delete all rubrics and all links.',
        md.hbold('For better understating how does interface work I ask you to try and explore more by yourself!'),
        'Interface is very simple and each step is going along with message.',
        md.hbold('Note:'),
        'Bot helps you to keep links.',
        'However it is possible also to save simple notes. Up to you.',
        md.hbold('Quick work:'),
        'For quick link adding just send a url [optionally, you can type after url some additional description]:',
        'https://getemoji.com/ and then your text that serves as link description.',
        'To pin link to some rubric you have to do this with main menu interaction.',
        md.hbold('Good luck!'),
        '🤖 I hope you`ll enjoy me!',
        sep='\n'
    )
    keyboard = LinksAndRubricsMainReplyKeyboard(one_time_keyboard=True)
    await message.answer(text, reply_markup=keyboard, disable_web_page_preview=True)


@dp.message_handler(commands=['cancel'], state='*')
async def command_cancel(message: types.Message, state: FSMContext):
    """ Cancel current action - reset state """
    await state.finish()

    keyboard = LinksAndRubricsMainReplyKeyboard(one_time_keyboard=True)
    await message.answer('❌ The current action has canceled!', reply_markup=keyboard)


@dp.message_handler(commands=['bug'])
@rate_limit(THROTTLING_RATE_LIMIT_IN_SECONDS_FOR_BUG_COMMAND)
async def command_bug(message: types.Message):
    """ Handle bug report from user """
    bug_message = message.get_args()

    try:
        bug_message = BugValidator().validate_bug_message(bug_message)
    except ValidationError as error:
        await message.answer(get_formatted_error_message(error))
    else:
        user_id = message.from_user.id

        bug = Bug(message=bug_message, user_id=user_id)
        async with async_db_sessionmaker() as session:
            await db.add_bug(session, bug)

        logger.info(f'Added new bug from @{message.from_user.username}')

        text = md.text(
            '✅ The bug report has been accepted!',
            md.hbold('Thank you! You care not only for bot 🤖 but also for your convenience!'),
            sep='\n'
        )
        keyboard = LinksAndRubricsMainReplyKeyboard(one_time_keyboard=True)

        await message.answer_sticker(STICKER_KISSING_FROG)
        await message.answer(text, reply_markup=keyboard)
