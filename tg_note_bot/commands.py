"""
Contains list of commands.

.. data:: COMMANDS
    List of the bot commands
"""

from aiogram.types import BotCommand


__all__ = ['COMMANDS']


start_command = BotCommand('start', 'Start interaction with bot')
help_command = BotCommand('help', 'Show help message')
cancel_command = BotCommand('cancel', 'Cancel current action')
bug_command = BotCommand('bug', 'Report about bug')


COMMANDS: list[BotCommand] = [
    start_command,
    help_command,
    cancel_command,
    bug_command
]
