"""
Contains common states groups.

.. class:: ManageSeriousDeletingStatesGroup(StatesGroup)
"""

from aiogram.dispatcher.filters.state import (
    State,
    StatesGroup
)


class ManageSeriousDeletingStatesGroup(StatesGroup):
    """ Implements delete managing states group """

    handling_of_delete_choice = State()
    handling_of_user_confirmation = State()
