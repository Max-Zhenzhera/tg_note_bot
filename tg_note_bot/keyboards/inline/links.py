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

        buttons: list[types.InlineKeyboardButton] = []

        for link in links:
            link_id = link.id
            link_url = link.short_url
            link_description = link.description
            link_rubric = link.rubric

            text = []

            if link_rubric:
                text.append(link_rubric.name)

            if link_description:
                text.append(f'({link_description})')

            text.append(link_url)
            text = ' '.join(text)

            button = types.InlineKeyboardButton(
                text,
                callback_data=LINK_CB.new(action=action, id=link_id)
            )
            buttons.append(button)

        super().__init__(*args, **kwargs)
        super().add(*buttons)
