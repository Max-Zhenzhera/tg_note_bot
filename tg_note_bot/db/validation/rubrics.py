"""
Contains validators for rubrics.

.. class:: RubricName(BaseModel)
    Rubric name validator
.. class:: RubricDescription(BaseModel)
    Rubric description validator
.. class:: RubricValidator
    Rubric validators joiner
"""

from typing import (
    Optional
)

from pydantic import (
    BaseModel,
    BaseConfig,
    Field
)


BaseConfig.anystr_strip_whitespace = True


class RubricName(BaseModel):
    rubric_name: str = Field(min_length=1, max_length=20)


class RubricDescription(BaseModel):
    rubric_description: Optional[str] = Field(max_length=200)


class RubricValidator:
    """
    Contains validators for rubric fields.
    As validation is implemented on Pydantic -> pydantic.ValidationError might be occur during validation.
    """

    RubricNameValidator = RubricName
    RubricDescriptionValidator = RubricDescription

    def validate_rubric_name(self, rubric_name: str) -> str:
        """
        Validate rubric name.

        :raises pydantic.ValidationError: raised if value is incorrect
        """

        rubric_name_validator_instance = self.RubricNameValidator(rubric_name=rubric_name)

        return rubric_name_validator_instance.rubric_name

    def validate_rubric_description(self, rubric_description: str) -> str:
        """
        Validate rubric description.

        :raises pydantic.ValidationError: raised if value is incorrect
        """

        rubric_description_validator_instance = self.RubricDescriptionValidator(rubric_description=rubric_description)

        return rubric_description_validator_instance.rubric_description
