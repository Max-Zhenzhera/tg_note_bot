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

    keyboard_structure_standard = [
        [button_to_set_none_rubric_for_links, button_to_delete_links, button_to_move_links_in_another_rubric]
    ]

    keyboard_structure_without_moving_decision = [
        [button_to_set_none_rubric_for_links, button_to_delete_links]
    ]

    def __init__(self, *args, does_user_have_other_rubrics: bool = True, **kwargs):
        """

        :param args:
        :type args:
        :keyword does_user_have_other_rubrics: offer to move related links in another rubric
            !only! if user has other rubrics
        :type does_user_have_other_rubrics: bool
        :param kwargs:
        :type kwargs:
        """

        if does_user_have_other_rubrics:
            super().__init__(self.keyboard_structure_standard, *args, **kwargs)
        else:
            super().__init__(self.keyboard_structure_without_moving_decision, *args, **kwargs)
