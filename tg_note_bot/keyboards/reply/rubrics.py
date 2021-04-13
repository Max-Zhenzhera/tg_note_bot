"""
Contains reply keyboards that related with rubrics.

.. class:: PossibleRubricEmojiNameReplyKeyboard(types.ReplyKeyboardMarkup)
.. class:: DecisionAboutRubricLinksOnDeletingReplyKeyboard(types.ReplyKeyboardMarkup)
"""

from aiogram import types


class PossibleRubricEmojiNameReplyKeyboard(types.ReplyKeyboardMarkup):
    """
    Implements keyboard with default rubrics name implemented as emojis
    """

    emojis_set = {
        '👍', '🤙', '🤟', '🤝',
        '📕', '💻', '🎓', '💼',
        '💡', '🎵', '📌', '⏳',
        '🌍', '🍓', '💋', '🤑',
    }

    def __init__(self, *args, except_emojis: set[str] = None, **kwargs):
        """
        :keyword except_emojis: from default `emojis_set` delete given set of rubric names
        :type except_emojis: set
        """

        emojis_set = self.emojis_set
        except_emojis = except_emojis if except_emojis else {None}
        emojis_set_to_use = emojis_set - except_emojis

        buttons = [types.KeyboardButton(emoji) for emoji in emojis_set_to_use]

        super().__init__(*args, **kwargs)
        self.add(*buttons)


class DecisionAboutRubricLinksOnDeletingReplyKeyboard(types.ReplyKeyboardMarkup):
    """
    Implements keyboard with choices to make decision about rubric links
    """

    text_for_button_to_set_none_rubric_for_links = '🖤 Set to non-rubric'
    text_for_button_to_delete_links = '🗑 Delete all related links'
    text_for_button_to_move_links_in_another_rubric = '📎 Move in another rubric'

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
        :keyword does_user_have_other_rubrics: offer to move related links in another rubric
            !only! if user has other rubrics
        :type does_user_have_other_rubrics: bool
        """

        if does_user_have_other_rubrics:
            super().__init__(self.keyboard_structure_standard, *args, **kwargs)
        else:
            super().__init__(self.keyboard_structure_without_moving_decision, *args, **kwargs)
