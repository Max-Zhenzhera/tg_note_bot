"""
Contains states groups for rubrics interactions.

.. class:: RubricAddingStatesGroup(StatesGroup)
"""

from aiogram.dispatcher.filters.state import State, StatesGroup


class RubricAddingStatesGroup(StatesGroup):
    """ Implements rubric adding states group """

    handling_of_rubric_name = State()
    handling_of_rubric_description = State()


class RubricDeletingStatesGroup(StatesGroup):
    """ Implements rubric deleting states group """

    handling_of_rubric_data = State()

    # offer to user to:
    # * delete all links related with this rubric
    # * throw all related links in non-rubric category [link without rubric]
    # * move rubric links in another rubric
    handling_of_decision_about_rubric_links = State()

    # if user has chosen to move rubric links in another rubric
    handling_of_new_rubric_to_move_links_into = State()
