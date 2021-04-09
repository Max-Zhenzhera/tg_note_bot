"""
Contains functions for setting up db.
"""

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine
)
from sqlalchemy.orm import sessionmaker

from .. import settings


def create_db_session() -> sessionmaker:
    """ Create async db session maker """
    engine = create_async_engine(
        f"{settings.DB_ENGINE}+{settings.DB_DRIVER}:///{settings.DB_PATH}",
        echo=settings.DEBUG_DB
    )
    async_session = sessionmaker(engine, class_=AsyncSession)

    return async_session


def create_db_engine() -> AsyncEngine:
    """ Create async db engine. Might me used for initializing """
    engine = create_async_engine(
        f"{settings.DB_ENGINE}+{settings.DB_DRIVER}:///{settings.DB_PATH}",
        echo=settings.DEBUG_DB
    )

    return engine
