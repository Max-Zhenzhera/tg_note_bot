"""
Entry point for db initializing and sql generation.
"""

import asyncio
import pathlib
import sys


# add package to global path -------------------------------------------------------------------------------------------
sys.path.append(pathlib.Path(__file__).parent.parent.__str__())
# ----------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    from database_initialization.init_db import main

    asyncio.run(
        main(
            to_drop_tables=False,
            to_create_tables=False,
            to_dump_sql_of_tables_creation=True
        )
    )
