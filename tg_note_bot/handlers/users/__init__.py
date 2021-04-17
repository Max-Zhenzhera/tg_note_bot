"""
Contains user handlers.
"""

from .basis import dp
from .data_managing import dp
from .rubrics import dp
from .links import dp

from .admin import dp

# catch all
from .other import dp

# from .test import dp


__all__ = ["dp"]
