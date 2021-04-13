"""
Contains common reply keyboards.

.. class:: EmptyValueReplyKeyboard(types.ReplyKeyboardMarkup)
.. class:: LinksAndRubricsMainReplyKeyboard(types.ReplyKeyboardMarkup)
"""

from aiogram import types

from ...settings import EMPTY_VALUE


class EmptyValueReplyKeyboard(types.ReplyKeyboardMarkup):
    """
    Implements keyboard with empty value button.
    """

    text_for_button_with_empty_value = EMPTY_VALUE
    button_with_empty_value = types.KeyboardButton(text_for_button_with_empty_value)

    keyboard_structure = [[button_with_empty_value]]

    def __init__(self, *args, **kwargs):
        super().__init__(self.keyboard_structure, *args, **kwargs)


class LinksAndRubricsMainReplyKeyboard(types.ReplyKeyboardMarkup):
    """
    Implements main keyboard for essential interactions.
    """

    # links section
    text_for_button_to_see_links = '👀 all links'
    text_for_button_to_dump_link = '🔎 link info'
    text_for_button_to_see_links_by_rubric = '🔎 links by rubric'
    text_for_button_to_add_link = '💾 link'
    text_for_button_to_delete_link = '🗑 link'
    text_for_button_to_manage_serious_deleting = '👊 Manage serious deleting 🔥'

    button_to_see_links = types.KeyboardButton(text_for_button_to_see_links)
    button_to_dump_link = types.KeyboardButton(text_for_button_to_dump_link)
    button_to_see_links_by_rubric = types.KeyboardButton(text_for_button_to_see_links_by_rubric)
    button_to_add_link = types.KeyboardButton(text_for_button_to_add_link)
    button_to_delete_link = types.KeyboardButton(text_for_button_to_delete_link)
    button_to_manage_serious_deleting = types.KeyboardButton(text_for_button_to_manage_serious_deleting)
    # -------------------------------------------------------------

    # rubrics section
    text_for_button_to_see_rubrics = '👀 all rubrics'
    text_for_button_to_add_rubric = '💾 rubric'
    text_for_button_to_delete_rubric = '🗑 rubric'

    button_to_see_rubrics = types.KeyboardButton(text_for_button_to_see_rubrics)
    button_to_add_rubric = types.KeyboardButton(text_for_button_to_add_rubric)
    button_to_delete_rubric = types.KeyboardButton(text_for_button_to_delete_rubric)
    # -------------------------------------------------------------

    keyboard_structure = [
        [button_to_see_links, button_to_add_link, button_to_delete_link],
        [button_to_see_rubrics, button_to_add_rubric, button_to_delete_rubric],
        [button_to_see_links_by_rubric, button_to_dump_link],
        [button_to_manage_serious_deleting]
    ]

    # -------------------------------------------------------------

    def __init__(self, *args, **kwargs):
        super().__init__(self.keyboard_structure, *args, **kwargs)


class ManageSeriousDeletingReplyKeyboard(types.ReplyKeyboardMarkup):
    """
    Implements keyboard for serious deleting options
    """

    text_for_button_to_delete_all_links = '🔥 all links'
    text_for_button_to_delete_all_rubrics = '🔥 all rubrics'
    text_for_button_to_delete_all_rubric_links = '🔥 all rubric links'
    text_for_button_to_delete_all_non_rubric_links = '🔥 all non-rubric links'
    text_for_button_to_delete_all = '🔥 all 🔥'

    button_to_delete_all_links = types.KeyboardButton(text_for_button_to_delete_all_links)
    button_to_delete_all_rubrics = types.KeyboardButton(text_for_button_to_delete_all_rubrics)
    button_to_delete_all_rubric_links = types.KeyboardButton(text_for_button_to_delete_all_rubric_links)
    button_to_delete_all_non_rubric_links = types.KeyboardButton(text_for_button_to_delete_all_non_rubric_links)
    button_to_delete_all = types.KeyboardButton(text_for_button_to_delete_all)

    keyboard_structure = [
        [button_to_delete_all_links, button_to_delete_all_rubrics],
        [button_to_delete_all_rubric_links, button_to_delete_all_non_rubric_links],
        [button_to_delete_all]
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(self.keyboard_structure, *args, **kwargs)
