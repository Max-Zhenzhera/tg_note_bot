"""
Entry point.
"""

import sys
import pathlib


# add package to global path -------------------------------------------------------------------------------------------
sys.path.append(pathlib.Path(__file__).parent.parent.__str__())
# ----------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    from tg_note_bot.app import main

    main()
