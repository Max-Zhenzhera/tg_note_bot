"""
Contains reply keyboards that related with rubrics.

.. class:: ecisionAboutRubricLinksOnDeletingReplyKeyboard(types.ReplyKeyboardMarkup)
"""

from aiogram import types


class DecisionAboutRubricLinksOnDeletingReplyKeyboard(types.ReplyKeyboardMarkup):
    """
    Implements keyboard with choices to make decision about rubric links
    """

    text_for_button_to_set_none_rubric_for_links = 'Set to non-rubric'
    text_for_button_to_delete_links = 'Delete all related links'
    text_for_button_to_move_links_in_another_rubric = 'Move in another rubric'

    button_to_set_none_rubric_for_links = types.KeyboardButton(text_for_button_to_set_none_rubric_for_links)
    button_to_delete_links = types.KeyboardButton(text_for_button_to_delete_links)
    button_to_move_links_in_another_rubric = types.KeyboardButton(text_for_button_to_move_links_in_another_rubric)

    keyboard_structure = [
        [button_to_set_none_rubric_for_links, button_to_delete_links, button_to_move_links_in_another_rubric]
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(self.keyboard_structure, *args, **kwargs)
