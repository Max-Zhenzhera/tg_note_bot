"""
Contains functions for setting up db.

.. func:: create_db_engine() -> AsyncEngine
    Create async db engine
.. func:: create_db_session() -> sessionmaker
    Create async db session maker
"""

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine
)
from sqlalchemy.orm import sessionmaker

from .. import settings


def create_db_engine() -> AsyncEngine:
    """ Create async sqlite db engine """
    engine = create_async_engine(
        f"{settings.DB_ENGINE}+{settings.DB_DRIVER}:///{settings.DB_PATH}",
        echo=settings.DEBUG_DB
    )

    return engine


def create_db_session() -> sessionmaker:
    """ Create async db session maker """
    engine = create_db_engine()
    async_session = sessionmaker(engine, class_=AsyncSession)

    return async_session
