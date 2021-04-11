"""
Implements db communication.
"""

from .db import (
    # adding
    add_entity,
    add_user,
    add_rubric,
    add_link,
    # deleting
    delete_entity_by_instance,
    delete_user,
    delete_rubric,
    delete_link,
    # fetching
    fetch_all_rubrics,
    fetch_one_rubric,
    fetch_all_links_without_rubric,
    # updating
    migrate_links_in_another_rubric,
    # aggregate
    does_rubric_have_any_links
)

from .errors import (
    TgNoteBotDbError,
    UserAlreadyInDbError
)

from .validation import (
    get_formatted_error_message,
    ValidationError,
    RubricValidator,
    LinkValidator
)
