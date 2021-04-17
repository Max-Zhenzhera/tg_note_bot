"""
Contains validators for rubrics.

.. class:: BugMessage(BaseModel)
    Bug message validator
.. class:: BugValidator
    Bug validators joiner
"""

from pydantic import (
    BaseModel,
    BaseConfig,
    Field
)


BaseConfig.anystr_strip_whitespace = True


class BugMessage(BaseModel):
    bug_message: str = Field(min_length=10, max_length=200)


class BugValidator:
    """
    Contains validators for bugs fields.
    As validation is implemented on Pydantic -> pydantic.ValidationError might be occur during validation.
    """

    BugMessageValidator = BugMessage

    def validate_bug_message(self, bug_message: str) -> str:
        """
        Validate rubric name.

        :raises pydantic.ValidationError: raised if value is incorrect
        """

        bug_message_validator_instance = self.BugMessageValidator(bug_message=bug_message)

        return bug_message_validator_instance.bug_message
