"""
Contains inline keyboards related with rubrics.

.. class:: RubricListInlineKeyboard(types.InlineKeyboardMarkup)

.. data:: RUBRIC_CB
    CallbackData
"""

from typing import (
    Optional
)

from aiogram import types
from aiogram.utils.callback_data import CallbackData

from ...settings import EMPTY_VALUE
from ...db.models import Rubric


# CB = callback data ------------------------------------------
RUBRIC_CB = CallbackData('rubric_data', 'action', 'id')
# -------------------------------------------------------------


class RubricListInlineKeyboard(types.InlineKeyboardMarkup):
    """
    Implements inline keyboard for the rubric list
    """

    def __init__(self, rubrics: list[Rubric],
                 *args,
                 action: str, empty_value_on_the_start: bool = False, except_rubrics_with_id: Optional[set[int]] = None,
                 **kwargs):
        """
        Build the inline keyboard with considering the additional arguments.
        Keyboard displays list of the rubrics.
        If `empty_value_on_the_start` argument was passed then on the top will be added `empty value` button.

        :param rubrics: list of the rubrics
        :type rubrics: list[Rubric]

        :param args: unnamed arguments that will be passed in simple `InlineKeyboardMarkup` constructor

        :keyword action: keyword that will be saved in `RUBRIC_CB['action']` callback data;
            help in filtering, so, it`s required.
        :type action: str
        :keyword empty_value_on_the_start: if passed button with empty value will be added on the top
        :type empty_value_on_the_start: bool
        :keyword except_rubrics_with_id: to remove particular rubrics from keyboard;
                                         might be used on links moving when deleting rubric should not be shown
        :type except_rubrics_with_id: Optional[set[int]]

        :param kwargs: named arguments that will be passed in simple `InlineKeyboardMarkup` constructor
        """

        buttons: list[types.InlineKeyboardButton] = []

        if except_rubrics_with_id is None:
            except_rubrics_with_id = set()

        if empty_value_on_the_start:
            buttons.append(types.InlineKeyboardButton(
                EMPTY_VALUE,
                callback_data=RUBRIC_CB.new(action=action, id=EMPTY_VALUE)
            ))

        for rubric in rubrics:
            rubric_id = rubric.id

            if rubric_id not in except_rubrics_with_id:
                text = rubric.name

                button = types.InlineKeyboardButton(
                    text,
                    callback_data=RUBRIC_CB.new(action=action, id=rubric_id)
                )
                buttons.append(button)

        super().__init__(*args, **kwargs)
        super().add(*buttons)
