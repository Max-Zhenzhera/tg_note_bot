"""
Contains handlers that have not caught before.

.. async:: handle_link_in_message(message: types.Message, regexp: re.Match) -> None
.. async:: catch_missed_text_message(message: types.Message) -> None
.. async:: catch_voice(message: types.Message) -> None
.. async:: catch_unhandled_message(message: types.Message) -> None
"""

import logging
import re

from aiogram import types
from aiogram.dispatcher.filters import Regexp
from aiogram.utils import markdown as md

from ... import db
from ...db import (
    get_formatted_error_message,
    ValidationError,
    LinkValidator
)
from ...db.models import Link
from ...loader import (
    dp,
    async_db_sessionmaker
)
from ...settings import STICKER_CONDEMNING_FROG
from ...utils.regexp import url_regexp


logger = logging.getLogger(__name__)


@dp.message_handler(Regexp(url_regexp))
async def handle_link_in_message(message: types.Message, regexp: re.Match) -> None:
    """ Catch link in message """
    user_id = message.from_user.id
    message_text = message.text

    url = regexp.group()
    start, end = regexp.start(), regexp.end()

    description = message_text[:start] + message_text[end:]
    description = description if description else None

    link_validator = LinkValidator()

    try:
        url, description = link_validator.validate_link_url(url), link_validator.validate_link_description(description)
    except ValidationError as error:
        text = f'I`ve caught your link but validation error has occured:\n{get_formatted_error_message(error)}'
        await message.answer(text)
    else:
        link = Link(url=url, description=description, user_id=user_id)
        link_repr = link.short_url_with_description

        async with async_db_sessionmaker() as session:
            await db.add_link(session, link)

        text = md.text(
            '✅ I`ve caught your link:',
            link_repr,
            'and added in non-rubric category. 😉',
            sep='\n'
        )
        await message.answer(text, disable_web_page_preview=True)


@dp.message_handler(content_types=types.ContentType.TEXT, state='*')
async def catch_missed_text_message(message: types.Message) -> None:
    """ Catch missed text message """
    text = md.text(
        '🤨 Sorry, but I don`t know what can I do with this:',
        f'Your message: {message.text}',
        '🤔 Try to get more with /help command!',
        f'🤖 {md.hbold("If this message has risen during simple menu interaction:")}',
        'Please, use the /bug command and describe situation.',
        'Example: /bug I`ve clicked on this button and nothing has happened',
        sep='\n'
    )
    await message.answer(text)


# funny one
@dp.message_handler(content_types=types.ContentType.VOICE, state='*')
async def catch_voice(message: types.Message) -> None:
    """ Catch voice message """
    await message.answer_sticker(STICKER_CONDEMNING_FROG)

    text = md.hitalic('It`s a bad habit to send voice messages. Especially to bot 😁')
    await message.answer(text)


@dp.message_handler(content_types=types.ContentType.ANY, state='*')
async def catch_unhandled_message(message: types.Message) -> None:
    """ Catch unhandled message """
    text = md.text(
        '🤨 Sorry, but I don`t know what can I do with this:',
        '🧐 It might be that you sent unsupported type of message (e.g. sticker, gif)',
        '🤔 Try to get more with /help command!',
        f'🤖 {md.hbold("If this message has risen during simple menu interaction:")}',
        'Please, use the /bug command and describe situation.',
        'Example: /bug I`ve clicked on this button and nothing has happened',
        sep='\n'
    )
    await message.answer(text)
