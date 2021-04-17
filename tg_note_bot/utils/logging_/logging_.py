"""
Contains functions for logging setup.
"""

import logging
import logging.config
import pathlib
from typing import (
    Union
)

import yaml

from ...settings import CORE_DIR


__all__ = ['setup_logging']


def _create_dirs_for_logs(config: dict) -> None:
    """ """
    for handler_name in config['handlers']:
        if 'file' in handler_name:
            log_path_from_main_package = config['handlers'][handler_name]['filename']
            log_path = (CORE_DIR / log_path_from_main_package).resolve()
            log_dir_path = log_path.parent
            log_dir_path.mkdir(parents=True, exist_ok=True)


def setup_logging(config_path: pathlib.Path, default_level: Union[int, str] = logging.INFO) -> None:
    """
    Setup logging.

    :param config_path: path to yaml file config
    :type config_path: pathlib.Path
    :param default_level: logging level that used if config setting is crashed
    :type default_level: Union[int, str]

    :return: None
    :rtype: None
    """

    if config_path.exists():
        with open(config_path, 'r') as config_file:
            try:
                config = yaml.safe_load(config_file.read())

                _create_dirs_for_logs(config)

                logging.config.dictConfig(config)
            except Exception as error:
                # here also might be set default logging
                raise error
    else:
        logging.basicConfig(level=default_level)

        logging.info('Failed to load the configuration file. Default config is using!')
