"""
Contains validators for links.

.. class:: LinkUrl(BaseModel)
    Rubric name validator
.. class:: LinkDescription(BaseModel)
    Rubric description validator
.. class:: LinkValidator
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


class LinkUrl(BaseModel):
    link: str = Field(min_length=3, max_length=200)


class LinkDescription(BaseModel):
    link_description: Optional[str] = Field(max_length=20)


class LinkValidator:
    """
    Contains validators for link fields.
    As validation is implemented on Pydantic -> pydantic.ValidationError might be occur during validation.
    """

    LinkUrlValidator = LinkUrl
    LinkDescriptionValidator = LinkDescription

    def validate_link_url(self, url: str) -> str:
        """
        Validate link name.

        :raises pydantic.ValidationError: raised if value is incorrect
        """

        link_validator_instance = self.LinkUrlValidator(link=url)

        return link_validator_instance.link

    def validate_link_description(self, link_description: str) -> str:
        """
        Validate link description.

        :raises pydantic.ValidationError: raised if value is incorrect
        """

        link_description_validator_instance = self.LinkDescriptionValidator(link_description=link_description)

        return link_description_validator_instance.link_description
