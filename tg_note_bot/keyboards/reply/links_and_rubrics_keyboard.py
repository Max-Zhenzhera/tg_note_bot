"""

"""

from aiogram import types


class LinksAndRubricsMainKeyboard(types.ReplyKeyboardMarkup):
    """
    Implements main keyboard for essential interactions.
    """

    # links section
    text_for_button_to_see_links = 'See all links'
    text_for_button_to_see_links_by_rubric = 'See links by rubric'
    text_for_button_to_add_link = 'Add a new link'
    text_for_button_to_delete_link = 'Delete the link'

    button_to_see_links = types.KeyboardButton(text_for_button_to_see_links)
    button_to_see_links_by_rubric = types.KeyboardButton(text_for_button_to_see_links_by_rubric)
    button_to_add_link = types.KeyboardButton(text_for_button_to_add_link)
    button_to_delete_link = types.KeyboardButton(text_for_button_to_delete_link)
    # -------------------------------------------------------------

    # rubrics section
    text_for_button_to_see_rubrics = 'See all rubrics'
    text_for_button_to_add_rubric = 'Add a new rubric'
    text_for_button_to_delete_rubric = 'Delete the rubric'

    button_to_see_rubrics = types.KeyboardButton(text_for_button_to_see_rubrics)
    button_to_add_rubric = types.KeyboardButton(text_for_button_to_add_rubric)
    button_to_delete_rubric = types.KeyboardButton(text_for_button_to_delete_rubric)
    # -------------------------------------------------------------

    # constructing buttons in the rows section
    keyboard_structure = [
        [button_to_see_links, button_to_see_rubrics],
        [button_to_see_links_by_rubric],
        [button_to_add_link, button_to_add_rubric],
        [button_to_delete_link, button_to_delete_rubric]
    ]

    # -------------------------------------------------------------

    def __init__(self, *args, **kwargs):
        super().__init__(self.keyboard_structure, *args, **kwargs)
