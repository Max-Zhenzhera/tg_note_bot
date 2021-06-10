"""
Contains db connection factories.
"""

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine
)
from sqlalchemy.orm import sessionmaker

from ..settings import (
    DB_CONNECTION_STRING,
    DEBUG_DB
)


__all__ = ['async_db_sessionmaker']


# https://docs.sqlalchemy.org/en/14/orm/session_basics.html

# # #
# When you write your application,
# the sessionmaker factory should be scoped the same as the Engine object created by create_engine(),
# which is typically at module-level or global scope.
# As these objects are both factories, they can be used by any number of functions and threads simultaneously.
# # #

engine = create_async_engine(DB_CONNECTION_STRING, echo=DEBUG_DB)
async_db_sessionmaker = sessionmaker(engine, class_=AsyncSession)
