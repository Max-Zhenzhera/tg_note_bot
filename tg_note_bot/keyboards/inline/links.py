"""
Contains inline keyboards related with links.

.. class:: LinkListInlineKeyboard(types.InlineKeyboardMarkup)

.. data:: LINK_CB
"""

from aiogram import types
from aiogram.utils.callback_data import CallbackData

from ...db.models import Link


# CB = callback data ------------------------------------------------
LINK_CB = CallbackData('link_data', 'action', 'id')
# -------------------------------------------------------------------


class LinkListInlineKeyboard(types.InlineKeyboardMarkup):
    """
    Implements inline keyboard for the link list
    """

    def __init__(self, links: list[Link], *args, action: str, **kwargs):
        """
        Build the inline keyboard with considering the additional arguments.
        Keyboard displays list of the links.

        :param rubrics: list of the rubrics
        :type rubrics: list[Rubric]

        :param args: unnamed arguments that will be passed in simple `InlineKeyboardMarkup` constructor

        :keyword action: keyword that will be saved in `LINK_CB['action']` callback data;
            help in filtering, so, it`s required.
        :type action: str

        :param kwargs: named arguments that will be passed in simple `InlineKeyboardMarkup` constructor
        """

        buttons = [
            types.InlineKeyboardButton(
                link.short_url_with_description_and_rubric,
                callback_data=LINK_CB.new(action=action, id=link.id)
            )
            for link in links
        ]

        super().__init__(*args, **kwargs)
        super().add(*buttons)
