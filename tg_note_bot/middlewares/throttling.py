"""
Contains throttling middleware implementation.

.. class:: ThrottlingMiddleware(BaseMiddleware)

.. decorator:: rate_limit
    Set particular rate limit for handler (anti-flood)

.. const:: THROTTLING_RATE_LIMIT_KEY
.. const:: THROTTLING_KEY
"""

import asyncio
from typing import (
    Callable,
    Optional
)

from aiogram import (
    Dispatcher,
    types
)
from aiogram.dispatcher import DEFAULT_RATE_LIMIT
from aiogram.dispatcher.handler import (
    CancelHandler,
    current_handler
)
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils.exceptions import Throttled


THROTTLING_RATE_LIMIT_KEY = 'throttling_rate_limit'
THROTTLING_KEY = 'throttling_key'


def rate_limit(limit: float, key: Optional[str] = None) -> Callable:
    """
    Decorator for configuring rate limit and key in different functions.

    :param limit: time limit in seconds
    :type limit: float
    :param key: throttling key
    :type key: Optional[str]

    :return: decorator
    :rtype: Callable
    """

    def decorator(func: Callable) -> Callable:
        """
        Set throttle attrs in handler.

        :param func: handler
        :type func: Callable
        :return: handler with set attrs
        :rtype: Callable
        """

        setattr(func, THROTTLING_RATE_LIMIT_KEY, limit)
        if key:
            setattr(func, THROTTLING_KEY, key)

        return func

    return decorator


class ThrottlingMiddleware(BaseMiddleware):
    """
    Implements anti-flood middleware
    """

    def __init__(self, limit: float = DEFAULT_RATE_LIMIT, key_prefix: str = 'antiflood_'):
        self.rate_limit = limit
        self.prefix = key_prefix

        super(ThrottlingMiddleware, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        """
        This handler is called when dispatcher receives a message.
        Manage messages to avoid flood.
        """

        handler = current_handler.get()
        dispatcher = Dispatcher.get_current()

        if handler:
            limit = getattr(handler, THROTTLING_RATE_LIMIT_KEY, self.rate_limit)
            key = getattr(handler, THROTTLING_KEY, f"{self.prefix}_{handler.__name__}")
        else:
            limit = self.rate_limit
            key = f"{self.prefix}_message"

        try:
            await dispatcher.throttle(key, rate=limit)
        except Throttled as t:
            await self.message_throttled(message, t)

            raise CancelHandler()

    async def message_throttled(self, message: types.Message, throttled: Throttled):
        """
        Notify user only on first exceed and notify about unlocking only on last exceed
        """

        handler = current_handler.get()
        dispatcher = Dispatcher.get_current()

        if handler:
            key = getattr(handler, THROTTLING_KEY, f"{self.prefix}_{handler.__name__}")
        else:
            key = f"{self.prefix}_message"

        delta = throttled.rate - throttled.delta

        if throttled.exceeded_count <= 2:
            await message.reply('Too many requests! Don`t flood, please!')

        await asyncio.sleep(delta)

        thr = await dispatcher.check_key(key)

        if thr.exceeded_count == throttled.exceeded_count:
            await message.reply('Unlocked. You can continue!')
