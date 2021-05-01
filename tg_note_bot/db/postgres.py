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

from ..settings import (
    DB_CONNECTION_STRING,
    DEBUG_DB
)


def create_db_engine() -> AsyncEngine:
    """ Create async postgres db engine """
    engine = create_async_engine(
        DB_CONNECTION_STRING,
        echo=DEBUG_DB
    )

    return engine


def create_db_session() -> sessionmaker:
    """ Create async db session maker """
    engine = create_db_engine()
    async_session = sessionmaker(engine, class_=AsyncSession)

    return async_session
