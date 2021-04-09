"""
Contains states groups for rubrics interactions.

.. class:: RubricAddingStatesGroup(StatesGroup)
.. class:: RubricDeletingStatesGroup(StatesGroup)
"""

from aiogram.dispatcher.filters.state import State, StatesGroup


class RubricAddingStatesGroup(StatesGroup):
    """ Implements rubric creation states group """

    handling_of_rubric_name = State()
    handling_of_rubric_description = State()


class RubricDeletingStatesGroup(StatesGroup):
    """ Implements rubric deleting states group """

    handling_of_rubric_id = State()
