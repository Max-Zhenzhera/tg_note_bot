"""
Initializes database.

.. func:: _get_sql_of_tables_creation(tables: list[Table]) -> str
.. func:: dump_in_file_sql_of_tables_creation(metadata: MetaData) -> None
.. async:: drop_tables(engine: AsyncEngine, metadata: MetaData) -> None
.. async:: create_tables(engine: AsyncEngine, metadata: MetaData) -> None
.. async:: main(*, to_drop_tables: bool = False, to_create_tables: bool = False,
        to_dump_sql_of_tables_creation: bool = True) -> None

.. const:: DIRECTORY_NAME_FOR_SQL_DUMP
.. const:: FILE_NAME_FOR_SQL_DUMP
"""

import datetime
import logging
import pathlib

from sqlalchemy import (
    MetaData,
    Table
)
from sqlalchemy.schema import CreateTable
from sqlalchemy.ext.asyncio import AsyncEngine

from tg_note_bot.db import (
    models,
    postgres
)


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(filename)s - %(funcName)s() [%(lineno)s] : %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


# CONSTANTS FOR SQL DUMP -----------------------------------------------------------------------------------------------
DIRECTORY_NAME_FOR_SQL_DUMP = 'sql'
FILE_NAME_FOR_SQL_DUMP = 'init.sql'
# ----------------------------------------------------------------------------------------------------------------------


def _get_sql_of_tables_creation(engine: AsyncEngine, tables: list[Table]) -> str:
    """
    Generate sql code for tables creation with added semi-columns.
    Might be used actually for dumping in file.

    :param engine: to generate sql code with db dialect considering
    :type engine: AsyncEngine
    :param tables: list of the tables
    :type tables: list[Table]

    :return: sql code of tables creations with added semi-columns
    :rtype: str
    """

    tables_creation_sql = '\n\n'.join(
        [
            str(CreateTable(table).compile(engine)).strip() + ';'
            for table in tables
        ]
    )

    return tables_creation_sql


def dump_in_file_sql_of_tables_creation(engine: AsyncEngine, metadata: MetaData) -> None:
    """
    Dump sql code of tables creation in file.

    Created for using in:
        - docker database container;
        - deploying.
    since it is a quick and correct way to init tables.

    :param engine: to generate sql code with db dialect considering
    :type engine: AsyncEngine
    :param metadata: metadata of the project models (Base.metadata)
    :type metadata: MetaData

    :return: None
    :rtype: None
    """

    directory_path_for_sql_dump = pathlib.Path(__file__).parent / DIRECTORY_NAME_FOR_SQL_DUMP
    directory_path_for_sql_dump.mkdir(exist_ok=True)

    filepath = directory_path_for_sql_dump / FILE_NAME_FOR_SQL_DUMP

    sql_dump = _get_sql_of_tables_creation(engine, metadata.sorted_tables)
    dump_comment = '\n'.join(
        (
            '/*',
            f'\tThis file is generated by `{__name__.split(".")[0]}` package.',
            f'\tVersion of the `models.py`: {models.__version__}',
            f'\tTime of the generation [UTC]: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
            '*/'
        )
    )

    with open(filepath, 'w') as file:
        file.write(dump_comment)
        file.write('\n\n\t/* The start of sql code */\n\n')
        file.write(sql_dump)

    logger.info(f'Sql dump of tables creation is created. To see - check {filepath}')


async def drop_tables(engine: AsyncEngine, metadata: MetaData) -> None:
    """
    Drop all tables by metadata (Base.metadata).

    :param engine: db engine
    :type engine: AsyncEngine
    :param metadata: metadata of the project models (Base.metadata)
    :type metadata: MetaData

    :return: None
    :rtype: None
    """

    async with engine.begin() as connection:
        await connection.run_sync(metadata.drop_all)

    logger.info('All tables have been deleted.')


async def create_tables(engine: AsyncEngine, metadata: MetaData) -> None:
    """
    Create all tables by metadata (Base.metadata).

    :param engine: db engine
    :type engine: AsyncEngine
    :param metadata: metadata of the project models (Base.metadata)
    :type metadata: MetaData

    :return: None
    :rtype: None
    """

    async with engine.begin() as connection:
        await connection.run_sync(metadata.create_all)

    logger.info('All tables have been created.')


async def main(*,
               to_drop_tables: bool = False,
               to_create_tables: bool = False,
               to_dump_sql_of_tables_creation: bool = True
               ) -> None:
    """
    Main coro, where might be executed:
        * dropping and creating of all tables;
        * dumping sql of tables creation.

    :keyword to_drop_tables: to drop all tables
    :type to_drop_tables: bool
    :keyword to_create_tables: to create all tables
    :type to_create_tables: bool
    :keyword to_dump_sql_of_tables_creation: to dump sql code of tables creation
    :type to_dump_sql_of_tables_creation: bool

    :return: None
    :rtype: None
    """

    engine = postgres.create_db_engine()
    metadata = models.Base.metadata

    if to_drop_tables or to_create_tables:
        if to_drop_tables:
            await drop_tables(engine, metadata)
        if to_create_tables:
            await create_tables(engine, metadata)

    if to_dump_sql_of_tables_creation:
        dump_in_file_sql_of_tables_creation(engine, metadata)
