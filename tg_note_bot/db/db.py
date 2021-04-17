"""
Contains functions that interact with db.

.. async:: add_entity(session: AsyncSession, entity: Base) -> None
.. async:: add_user(session: AsyncSession, user: User) -> None
.. async:: add_rubric(session: AsyncSession, rubric: Rubric) -> None
.. async:: add_link(session: AsyncSession, link: Link) -> None
.. async:: add_bug(session: AsyncSession, bug: Bug) -> None

.. async:: fetch_one_rubric(session: AsyncSession, rubric_id: int, *, with_links: bool = False) -> Rubric
.. async:: fetch_all_rubrics(session: AsyncSession, user_id: int, *, with_links: bool = False) -> list[Rubric]
.. async:: fetch_one_link(session: AsyncSession, link_id: int, *, with_rubric: bool = True) -> Link
.. async:: fetch_all_links(session: AsyncSession, user_id: int, *, with_rubric: bool = False,
        group_by_rubric: bool = False) -> Union[list[Link], dict[Optional[Rubric], Link]]
.. async:: fetch_all_bugs(session: AsyncSession) -> list[Bug]
.. async:: fetch_all_unwatched_bugs(session: AsyncSession) -> list[Bug]

.. async:: migrate_links_in_another_rubric(session: AsyncSession, old_rubric_id: int, new_rubric_id: int) -> None
.. async:: mark_all_bugs_as_watched(session: AsyncSession) -> None

.. async:: delete_entity_by_instance(session: AsyncSession, entity: Base) -> None
.. async:: delete_user(session: AsyncSession, user_id: int) -> None
.. async:: delete_one_rubric(session: AsyncSession, rubric_id: int, *, delete_links: bool = False,
        migrate_links_in_rubric_with_id: int = False) -> None
.. async:: delete_all_rubrics(session: AsyncSession, user_id: int, *, delete_links: bool = False) -> None
.. async:: delete_one_link(session: AsyncSession, link_id: int) -> None
.. async:: delete_all_links_by_user(session: AsyncSession, user_id: int) -> None
.. async:: delete_all_rubric_links_by_user(session: AsyncSession, user_id: int) -> None
.. async:: delete_all_non_rubric_links_by_user(session: AsyncSession, user_id: int) -> None
.. async:: delete_all_links_by_rubric(session: AsyncSession, rubric_id: int) -> None
.. async:: delete_all_user_data(session: AsyncSession, user_id: int) -> None

.. async:: count_user_rubrics(session: AsyncSession, user_id: int) -> int
.. async:: does_rubric_have_any_links(session: AsyncSession, rubric_id: int) -> bool
.. async:: does_rubric_have_unique_name(session: AsyncSession, user_id: int, rubric_name: str) -> bool

.. async:: count_bot_users(session: AsyncSession) -> int
"""

import itertools
import logging
import operator
from typing import (
    Optional,
    Union
)

import sqlalchemy as sa
from sqlalchemy import exc
from sqlalchemy.future import select
from sqlalchemy.orm import (
    joinedload,
    selectinload
)
from sqlalchemy.ext.asyncio import AsyncSession

from .models import (
    Base,
    User,
    Rubric,
    Link,
    Bug
)
from .errors import UserAlreadyInDbError


logger = logging.getLogger(__name__)


# create ---------------------------------------------------------------------------------------------------------------
async def add_entity(session: AsyncSession, entity: Base) -> None:
    """
    Execute statement [add instance to session] and commit transaction.

    :param session: db connection
    :type session: AsyncSession
    :param entity: one of Base models instance
    :type entity: Base

    :return: None
    :rtype: None
    """

    async with session.begin():
        session.add(entity)


# # User
async def add_user(session: AsyncSession, user: User) -> None:
    """
    Add user.

    :param session: db connection
    :type session: AsyncSession
    :param user: User instance
    :type user: User

    :return: None
    :rtype: None

    :raises UserAlreadyInDbError: raised if user with same id exists in db
    """

    try:
        await add_entity(session, user)
    except sa.exc.IntegrityError:
        logger.debug(f'|user adding| User with <id={User.id}> has already been in the database.')

        raise UserAlreadyInDbError
    else:
        logger.debug(f'|user adding| User with <id={User.id}> has been added in the database.')


# # Rubric
async def add_rubric(session: AsyncSession, rubric: Rubric) -> None:
    """
    Add rubric.
    The same as `add_entity` function, but more clear.

    :param session: db connection
    :type session: AsyncSession
    :param rubric: Rubric instance
    :type rubric: Rubric

    :return: None
    :rtype: None
    """

    await add_entity(session, rubric)


# # Link
async def add_link(session: AsyncSession, link: Link) -> None:
    """
    Add link.
    The same as `add_entity` function, but more clear.

    :param session: db connection
    :type session: AsyncSession
    :param link: Link instance
    :type link: Link

    :return: None
    :rtype: None
    """

    await add_entity(session, link)


# # Bug
async def add_bug(session: AsyncSession, bug: Bug) -> None:
    """
    Add bug.
    The same as `add_entity` function, but more clear.

    :param session: db connection
    :type session: AsyncSession
    :param bug: Bug instance
    :type bug: Bug

    :return: None
    :rtype: None
    """

    await add_entity(session, bug)
# ----------------------------------------------------------------------------------------------------------------------


# read -----------------------------------------------------------------------------------------------------------------
# # Rubric
async def fetch_one_rubric(session: AsyncSession, rubric_id: int, *, with_links: bool = False) -> Rubric:
    """
    Fetch one rubric. Optionally, might be loaded rubric links.

    :param session: db connection
    :type session: AsyncSession
    :param rubric_id: rubric id
    :type rubric_id: int
    :keyword with_links: to load rubric links
    :type with_links: bool

    :return: rubric
    :rtype: Rubric
    """

    if with_links:
        stmt = select(Rubric).options(selectinload(Rubric.links)).where(Rubric.id == rubric_id)
    else:
        stmt = select(Rubric).where(Rubric.id == rubric_id)

    result = await session.execute(stmt)
    rubric = result.scalar()

    return rubric


async def fetch_all_rubrics(session: AsyncSession, user_id: int, *, with_links: bool = False) -> list[Rubric]:
    """
    Fetch all rubrics. Optionally, might be loaded rubric links.

    :param session: db connection
    :type session: AsyncSession
    :param user_id: user id
    :type user_id: int
    :keyword with_links: to load rubric links
    :type with_links: bool

    :return: rubrics
    :rtype: list[Rubric]
    """

    if with_links:
        stmt = select(Rubric).options(selectinload(Rubric.links)).where(Rubric.user_id == user_id).order_by(Rubric.name)
    else:
        stmt = select(Rubric).where(Rubric.user_id == user_id).order_by(Rubric.name)

    result = await session.execute(stmt)
    rubrics = list(result.scalars())

    return rubrics


# # Link
async def fetch_one_link(session: AsyncSession, link_id: int, *, with_rubric: bool = True) -> Link:
    """
    Fetch one link. Optionally, might be rubric loaded.

    :param session: db connection
    :type session: AsyncSession
    :param link_id: link id
    :type link_id: int
    :param with_rubric: to load link`s rubric
    :type with_rubric: bool

    :return: link
    :rtype: Link
    """

    if with_rubric:
        stmt = select(Link).options(joinedload(Link.rubric)).where(Link.id == link_id)
    else:
        stmt = select(Link).where(Link.id == link_id)

    result = await session.execute(stmt)
    link = result.scalar()

    return link


async def fetch_all_links(session: AsyncSession, user_id: int,
                          *,
                          with_rubric: bool = False, group_by_rubric: bool = False
                          ) -> Union[list[Link], dict[Optional[Rubric], Link]]:
    """
    Fetch all links. Optionally, result might be grouped by link`s rubrics or simply loaded with rubric data.

    :param session: db connection
    :type session: AsyncSession
    :param user_id: user id
    :type user_id: int
    :keyword with_rubric: to join rubric data to link
    :type with_rubric: bool
    :keyword group_by_rubric: to return links grouped by rubrics
        [with this flag - flag `with_rubric` will be turned in automatically]
    :type group_by_rubric: bool

    :return: links
    :rtype: Union[list[Link], dict[Optional[Rubric], Link]]
    """

    with_rubric = True if group_by_rubric else with_rubric

    if with_rubric:
        stmt = select(Link).options(joinedload(Link.rubric)).where(Link.user_id == user_id)
    else:
        stmt = select(Link).where(Link.user_id == user_id).order_by(Link.rubric_id)

    result = await session.execute(stmt)
    links = list(result.scalars())

    if group_by_rubric:
        # assert that rubric data is loaded
        rubric_attr_name_in_link = 'rubric'

        links = {
            rubric: list(rubric_links)
            for rubric, rubric_links in itertools.groupby(links, operator.attrgetter(rubric_attr_name_in_link))
        }

    return links


# # Bug
async def fetch_all_bugs(session: AsyncSession) -> list[Bug]:
    """
    Fetch all bugs.

    :param session: db connection
    :type session: AsyncSession

    :return: all bugs
    :rtype: list[Bug]
    """

    stmt = select(Bug)
    result = await session.execute(stmt)
    bugs = list(result.scalars())

    return bugs


async def fetch_all_unwatched_bugs(session: AsyncSession) -> list[Bug]:
    """
    Fetch all unwatched bugs.

    :param session:
    :type session:

    :return: all unwatched bugs
    :rtype: list[Bug]
    """

    stmt = select(Bug).where(Bug.is_shown == False)
    result = await session.execute(stmt)
    bugs = list(result.scalars())

    return bugs
# ----------------------------------------------------------------------------------------------------------------------


# update ---------------------------------------------------------------------------------------------------------------
# # Link
async def migrate_links_in_another_rubric(session: AsyncSession, old_rubric_id: int, new_rubric_id: int) -> None:
    """
    Move all links from ine rubric in another rubric.

    :param session: db connection
    :type session: AsyncSession
    :param old_rubric_id: move links !from! this rubric
    :type old_rubric_id: int
    :param new_rubric_id: move links !in! this rubric
    :type new_rubric_id: int

    :return: None
    :rtype: None
    """

    async with session.begin():
        stmt = (
            sa.update(Link).
            where(Link.rubric_id == old_rubric_id).
            values(rubric_id=new_rubric_id)
        )
        await session.execute(stmt)


# # Bug
async def mark_all_bugs_as_watched(session: AsyncSession) -> None:
    """
    Mark all bugs as watched.

    :param session: db connection
    :type session: AsyncSession

    :return: None
    :rtype: None
    """

    async with session.begin():
        stmt = sa.update(Bug).values(is_shown=True)
        await session.execute(stmt)
# ----------------------------------------------------------------------------------------------------------------------


# delete ---------------------------------------------------------------------------------------------------------------
async def delete_entity_by_instance(session: AsyncSession, entity: Base) -> None:
    """
    Delete entity by model instance.

    :param session: db connection
    :type session: AsyncSession
    :param entity: model instance
    :type entity: Base

    :return: None
    :rtype: None
    """

    async with session.begin():
        await session.delete(entity)


# # User
async def delete_user(session: AsyncSession, user_id: int) -> None:
    """
    Delete user.

    :param session: db connection
    :type session: AsyncSession
    :param user_id: user id [as `User` keeps `id` column - means user tg id]
    :type user_id: int

    :return: None
    :rtype: None
    """

    async with session.begin():
        stmt = sa.delete(User).where(User.id == user_id)
        await session.execute(stmt)


# # Rubric
async def delete_one_rubric(session: AsyncSession, rubric_id: int,
                            *,
                            delete_links: bool = False, migrate_links_in_rubric_with_id: int = False
                            ) -> None:
    """
    Delete rubric. Optionally, it is possible to:
        * migrate related links in non-rubric category [by default]
        * delete related links [with `delete_links` flag]
        * migrate related links in another rubric [with `migrate_links_in_rubric_with_id` int id value]

    Note:
        It is impossible to pass few arguments that make different operating with related links.

    :param session: db connection
    :type session: AsyncSession
    :param rubric_id: rubric id
    :type rubric_id: int
    :keyword delete_links: to delete rubric and links that related with this rubric
    :type delete_links: bool
    :keyword migrate_links_in_rubric_with_id: to delete rubric and migrate related links in another rubric
    :type migrate_links_in_rubric_with_id: int

    :return: None
    :rtype: None

    :raises TypeError: raised if few arguments that make different operating with related links have passed
    """

    if delete_links and migrate_links_in_rubric_with_id:
        msg = (
            'It is impossible to pass few arguments that make different operating with related links! '
            'Instead got <delete_links> and <migrate_links_in_rubric_with_id> arguments together.'
        )
        raise TypeError(msg)
    elif delete_links:
        await delete_all_links_by_rubric(session, rubric_id=rubric_id)
    elif migrate_links_in_rubric_with_id:
        await migrate_links_in_another_rubric(session, rubric_id, migrate_links_in_rubric_with_id)

    async with session.begin():
        stmt = sa.delete(Rubric).where(Rubric.id == rubric_id)
        await session.execute(stmt)


async def delete_all_rubrics(session: AsyncSession, user_id: int, *, delete_links: bool = False) -> None:
    """
    Delete all rubrics.
    Optionally, it is possible to delete all links that related with rubrics [with `delete_links` flag].

    :param session: db connection
    :type session: AsyncSession
    :param user_id: user id
    :type user_id: int
    :param delete_links: to delete links that related with rubrics
    :type delete_links: bool

    :return: None
    :rtype: None
    """

    if delete_links:
        await delete_all_rubric_links_by_user(session, user_id)

    async with session.begin():
        stmt = sa.delete(Rubric).where(Rubric.user_id == user_id)
        await session.execute(stmt)


# # Link
async def delete_one_link(session: AsyncSession, link_id: int) -> None:
    """
    Delete link.

    :param session: db connection
    :type session: AsyncSession
    :param link_id: link id
    :type link_id: int

    :return: None
    :rtype: None
    """

    async with session.begin():
        stmt = sa.delete(Link).where(Link.id == link_id)
        await session.execute(stmt)


async def delete_all_links_by_user(session: AsyncSession, user_id: int) -> None:
    """
    Delete all links that related with user.

    :param session: db connection
    :type session: AsyncSession
    :param user_id: user id
    :type user_id: int

    :return: None
    :rtype: None
    """

    async with session.begin():
        stmt = sa.delete(Link).where(Link.user_id == user_id)
        await session.execute(stmt)


async def delete_all_links_by_rubric(session: AsyncSession, rubric_id: int) -> None:
    """
    Delete all links that related with rubric.

    :param session: db connection
    :type session: AsyncSession
    :param rubric_id: rubric id

    :type rubric_id: int
    :return: None
    :rtype: None
    """

    async with session.begin():
        stmt = sa.delete(Link).where(Link.rubric_id == rubric_id)
        await session.execute(stmt)


async def delete_all_rubric_links_by_user(session: AsyncSession, user_id: int) -> None:
    """
    Delete all links that have rubric and related with user.

    :param session: db connection
    :type session: AsyncSession
    :param user_id: user id
    :type user_id: int

    :return: None
    :rtype: None
    """

    async with session.begin():
        stmt = sa.delete(Link).where(sa.and_(Link.user_id == user_id, Link.rubric_id != None))
        await session.execute(stmt)


async def delete_all_non_rubric_links_by_user(session: AsyncSession, user_id: int) -> None:
    """
    Delete all non-rubric links that related with user.

    :param session: db connection
    :type session: AsyncSession
    :param user_id: user id
    :type user_id: int

    :return: None
    :rtype: None
    """

    async with session.begin():
        stmt = sa.delete(Link).where(sa.and_(Link.user_id == user_id, Link.rubric_id == None))
        await session.execute(stmt)


async def delete_all_user_data(session: AsyncSession, user_id: int) -> None:
    """
    Delete all links and rubrics that related with user.

    :param session: db connection
    :type session: AsyncSession
    :param user_id: user id
    :type user_id: int

    :return: None
    :rtype: None
    """

    await delete_all_links_by_user(session, user_id)
    await delete_all_rubrics(session, user_id)
# ----------------------------------------------------------------------------------------------------------------------


# aggregate ------------------------------------------------------------------------------------------------------------
async def count_user_rubrics(session: AsyncSession, user_id: int) -> int:
    """
    Return quantity of the user rubrics.

    :param session: db connection
    :type session: AsyncSession
    :param user_id: user id
    :type user_id: int

    :return: user rubrics quantity
    :rtype: int
    """

    stmt = select(sa.func.count()).select_from(Rubric).where(Rubric.user_id == user_id)
    result = await session.execute(stmt)
    user_rubrics_quantity = result.scalar()

    return user_rubrics_quantity


async def does_rubric_have_any_links(session: AsyncSession, rubric_id: int) -> bool:
    """
    Check that rubric has any links.

    :param session: db connection
    :type session: AsyncSession
    :param rubric_id: rubric id
    :type rubric_id: int

    :return: does rubric have any links flag
    :rtype: bool
    """

    stmt = select(Link).where(Link.rubric_id == rubric_id)
    result = await session.execute(stmt)
    flag = True if result.first() else False

    return flag


async def does_rubric_have_unique_name(session: AsyncSession, user_id: int, rubric_name: str) -> bool:
    """
    Check that exists rubric with name.

    :param session: db connection
    :type session: AsyncSession
    :param user_id: user id
    :type user_id: int
    :param rubric_name: rubric name
    :type rubric_name: int

    :return: True if no one rubric exists with this name else False
    :rtype: bool
    """

    stmt = select(Rubric).where(sa.and_(Rubric.user_id == user_id, Rubric.name == rubric_name))
    result = await session.execute(stmt)
    flag = False if result.first() else True

    return flag


# # Statistic for admin
async def count_bot_users(session: AsyncSession) -> int:
    """
    Return quantity of the bot users.

    :param session: db connection
    :type session: AsyncSession

    :return: users quantity
    :rtype: int
    """

    stmt = select(sa.func.count()).select_from(User)
    result = await session.execute(stmt)
    users_quantity = result.scalar()

    return users_quantity
