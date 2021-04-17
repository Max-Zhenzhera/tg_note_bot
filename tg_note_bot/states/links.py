"""
Contains states groups for rubrics interactions.

.. class:: LinkAddingStatesGroup(StatesGroup)
"""

from aiogram.dispatcher.filters.state import (
    State,
    StatesGroup
)


class LinkAddingStatesGroup(StatesGroup):
    """ Implements link adding states group """

    handling_of_link_url = State()
    handling_of_link_description = State()
    handling_of_link_rubric = State()
