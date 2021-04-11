"""
Contains functions that interact with db.

.. async:: add_entity(session: AsyncSession, entity: Base) -> None
.. async:: add_user(session: AsyncSession, user: User) -> None
.. async:: add_rubric(session: AsyncSession, rubric: Rubric) -> None
.. async:: add_link(session: AsyncSession, link: Link) -> None

.. async:: delete_entity_by_instance(session: AsyncSession, entity: Base) -> None
.. async:: delete_user(session: AsyncSession, user_id: int) -> None
.. async:: delete_rubric(session: AsyncSession, rubric_id: int, *, delete_links: bool = False) -> None
.. async:: delete_link(session: AsyncSession, link_id: int) -> None

.. async:: fetch_all_rubrics(session: AsyncSession, user_id: int, *, with_links: bool = False) -> list[Rubric]
.. async:: fetch_one_rubric(session: AsyncSession, rubric_id: int, *, with_links: bool = False) -> Rubric
.. async:: fetch_all_links_without_rubric(session: AsyncSession, user_id: int) -> list[Link]
"""

import logging

import sqlalchemy as sa
from sqlalchemy import exc
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from .models import (
    Base,
    User,
    Rubric,
    Link
)
from .errors import UserAlreadyInDbError


logger = logging.getLogger(__name__)


# adding ---------------------------------------------------------------------------------------------------------------
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
    except sa.exc.IntegrityError as error:
        logger.debug(f'|user adding| User with <id={User.id}> has already been in the database.')

        raise UserAlreadyInDbError from error
    else:
        logger.debug(f'|user adding| User with <id={User.id}> has been added in the database.')


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
# ----------------------------------------------------------------------------------------------------------------------


# deleting -------------------------------------------------------------------------------------------------------------
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


async def delete_user(session: AsyncSession, user_id: int) -> None:
    """
    Delete user.

    :param session: db connection
    :type session: AsyncSession
    :param user_id: user id [as `User` keeps `tg_id` column - means user tg id]
    :type user_id: int

    :return: None
    :rtype: None
    """

    async with session.begin():
        stmt = sa.delete(User).where(User.id == user_id)
        await session.execute(stmt)


async def delete_rubric(session: AsyncSession, rubric_id: int, *, delete_links: bool = False) -> None:
    """
    Delete rubric. Also, optionally, delete rubric links.

    :param session: db connection
    :type session: AsyncSession
    :param rubric_id: rubric id
    :type rubric_id: int
    :keyword delete_links: to delete rubric links [by default links move on non rubric section]
    :type delete_links: bool

    :return: None
    :rtype: None
    """

    async with session.begin():
        if delete_links:
            stmt = sa.delete(Link).where(Link.rubric_id == rubric_id)
            await session.execute(stmt)

        stmt = sa.delete(Rubric).where(Rubric.id == rubric_id)
        await session.execute(stmt)


async def delete_link(session: AsyncSession, link_id: int) -> None:
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
# ----------------------------------------------------------------------------------------------------------------------


# fetching -------------------------------------------------------------------------------------------------------------
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


async def fetch_all_links_without_rubric(session: AsyncSession, user_id: int) -> list[Link]:
    """
    Fetch all links without rubric.
    Supposed to be invoked after `fetch_all_rubrics(with_links=True)`,
    such this a quick way to get links ordered by rubrics.

    :param session: db connection
    :type session: AsyncSession
    :param user_id: user id
    :type user_id: int

    :return: rubrics
    :rtype: list[Link]
    """

    stmt = select(Link).where(Link.user_id == None).order_by(Link.url)
    result = await session.execute(stmt)
    links = list(result.scalars())

    return links
# ----------------------------------------------------------------------------------------------------------------------


# updating -------------------------------------------------------------------------------------------------------------
async def migrate_links_in_another_rubric(session: AsyncSession, user_id: int, old_rubric_id: int, new_rubric_id: int
                                          ) -> None:
    """
    Move all links in another rubric.

    :param session: db connection
    :type session: AsyncSession
    :param user_id: user_id
    :type user_id: int
    :param old_rubric_id: update links !with! this rubric
    :type old_rubric_id: int
    :param new_rubric_id: update links !on! this rubric
    :type new_rubric_id: int

    :return: None
    :rtype: None
    """

    stmt = (
        sa.update(Link).
        where(
            sa.and_(
                Link.user_id == user_id,
                Link.rubric_id == old_rubric_id
            )
        ).
        values(rubric_id=new_rubric_id)
    )
    await session.execute(stmt)
# ----------------------------------------------------------------------------------------------------------------------


# aggregate ------------------------------------------------------------------------------------------------------------
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
    flag = True if result.one_or_none() else False

    return flag
