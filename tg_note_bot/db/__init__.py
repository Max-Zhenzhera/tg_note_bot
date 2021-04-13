"""
Implements db communication.
"""

from .db import (
    # create
    add_entity,
    add_user,
    add_rubric,
    add_link,
    # read
    fetch_one_rubric,
    fetch_all_rubrics,
    fetch_one_link,
    fetch_all_links,
    # update
    migrate_links_in_another_rubric,
    # delete
    delete_entity_by_instance,
    delete_user,
    delete_one_rubric,
    delete_all_rubrics,
    delete_one_link,
    delete_all_links_by_user,
    delete_all_rubric_links_by_user,
    delete_all_non_rubric_links_by_user,
    delete_all_links_by_rubric,
    # aggregate
    count_user_rubrics,
    does_rubric_have_any_links,
    does_rubric_have_unique_name,
    # admin
    count_bot_users
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
