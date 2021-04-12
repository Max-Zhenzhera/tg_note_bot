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
    fetch_all_links,
    fetch_one_link,
    fetch_all_links_without_rubric,
    fetch_all_links_with_rubric_grouping,
    # updating
    migrate_links_in_another_rubric,
    # aggregate
    count_user_rubrics,
    does_rubric_have_any_links,
    does_rubric_have_unique_name
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
