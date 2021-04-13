"""
Contains settings.

.. const:: BASE_DIR
.. const:: CORE_DIR

.. const:: LOGGING_CONFIG_PATH
.. const:: DEBUG_DB

.. const:: BOT_TOKEN

.. const:: DB_ENGINE
.. const:: DB_DRIVER
.. const:: DB_NAME
.. const:: DB_PATH
"""

import os
import pathlib

from dotenv import load_dotenv


# LOAD ENV  /////////////////////////////////////////////////////////////////////////////////////////////////
load_dotenv()
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

# PATH SETTINGS /////////////////////////////////////////////////////////////////////////////////////////////
BASE_DIR = pathlib.Path(__file__).parent.parent
CORE_DIR = pathlib.Path(__file__).parent
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

# LOGGING - DEBUGGING ///////////////////////////////////////////////////////////////////////////////////////
LOGGING_CONFIG_PATH = CORE_DIR / 'utils' / 'logging_' / 'logging_config.yaml'

DEBUG_DB = True
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

# API TOKENS ////////////////////////////////////////////////////////////////////////////////////////////////
BOT_TOKEN = os.getenv('TG_BOT_TOKEN')
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

# DB SETTINGS ///////////////////////////////////////////////////////////////////////////////////////////////
DB_ENGINE = os.getenv('DB_ENGINE')
DB_DRIVER = os.getenv('DB_DRIVER')
DB_NAME = os.getenv('DB_NAME')

DB_PATH = BASE_DIR / f'{DB_NAME}.db'
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

# BOT VARS //////////////////////////////////////////////////////////////////////////////////////////////////
ADMINS: list[int] = [int(admin_id) for admin_id in os.getenv('ADMINS').split(',')]
THROTTLING_RATE_LIMIT_IN_SECONDS: float = .2

EMPTY_VALUE = '➡️ Pass'
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

# USED EMOJIS ///////////////////////////////////////////////////////////////////////////////////////////////
NON_RUBRIC_CATEGORY = '🖤'   # also rubric shift

TO_SEE = '👀'
TO_CREATE = '💾'
TO_DELETE = '🗑'
TO_DO_SERIOUS_DELETE = '👊', '🔥'

RUBRIC_SHIFT = '🔘'
LINK_SHIFT = '👉'
INPUT_ARGUMENT = '📝'
ARGUMENT_ACCEPTED = '👌'
ARGUMENT_UNIQUE = '🔑'
ARGUMENT_REQUIRED = '❗️'    # !
ARGUMENT_OPTIONAL = '🆓'
ERROR_OCCURED = '🛑'
REQUEST_EXECUTED = '☑️ '    # grey ✅
ACTION_COMPLETED = '✅'
CHOOSE_CHOICE = '❔'
EMPTY_RESULT = '🕳'
TIME_POINT = '🧭'
NOTE_MESSAGE = '💿'
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
