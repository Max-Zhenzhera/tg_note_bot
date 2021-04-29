"""
Test
"""

import asyncio
import os
import itertools as it
import operator

import dotenv
import sqlalchemy as sa
from sqlalchemy.future import select
from sqlalchemy.orm import (
    selectinload,
    joinedload,
    Query
)
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession
)

from tg_note_bot.db import (
    models,
    postgres,
    db
)


dotenv.load_dotenv()


async def main():
    pass


if __name__ == '__main__':
    asyncio.run(main())
