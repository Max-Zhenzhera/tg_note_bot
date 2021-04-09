"""
Contains validators.
"""

from typing import (
    Optional
)

import pydantic

from .rubrics import RubricValidator


ValidationError = pydantic.ValidationError


def get_formatted_error_message(validation_error: pydantic.ValidationError,
                                error_message_prefix: Optional[bool] = True
                                ) -> str:
    """
    Return formatted message about validation errors.

    :param validation_error: error that was raised on validation
    :type validation_error: pydantic.ValidationError
    :param error_message_prefix: `Incorrect input!` prefix on the start is included by
    :type error_message_prefix: Optional[bool]

    :return: formatted, user readable message
    :rtype: str
    """

    error_messages = ['Incorrect input!'] if error_message_prefix else []

    for error in validation_error.errors():
        error_location: str = error['loc'][0]        # ruined attr name
        error_message: str = error['msg']

        formatted_error_location = ' '.join(error_location.split('_')).capitalize()
        formatted_error_message = f'{formatted_error_location}: {error_message}'

        error_messages.append(formatted_error_message)

    message = '\n'.join(error_messages)

    return message
