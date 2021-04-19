"""
Test
"""
import asyncio

import yarl
import sqlalchemy as sa
from sqlalchemy.future import select
from tg_note_bot.db import models, postgres, db
from tg_note_bot.db.models import *
from sqlalchemy.orm import selectinload, joinedload, Query
from sqlalchemy import engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.collections import InstrumentedList
import itertools as it
import operator
async_session = postgres.create_db_session()


async def main():
    session: AsyncSession
    async with async_session() as session:
        async with session.begin():
            stmt = select(User).options(selectinload(User.rubrics)).options(selectinload(User.links)).where(User.id == 692001589)
            r = await session.execute(stmt)
            a = r.scalar()
            print(a)
            print(a.rubrics)
            print(a.links)



if __name__ == '__main__':
    asyncio.run(main())
