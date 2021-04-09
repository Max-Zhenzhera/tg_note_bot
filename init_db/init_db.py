"""
Initializes database.

.. func:: main()
    Manage the tables.
"""

import asyncio

from tg_note_bot.db import (
    models,
    sqlite
)


async def main():
    """ Drop and create all tables """
    engine = sqlite.create_db_engine()

    async with engine.begin() as connection:
        await connection.run_sync(models.Base.metadata.drop_all)
        await connection.run_sync(models.Base.metadata.create_all)


if __name__ == '__main__':
    asyncio.run(main())
