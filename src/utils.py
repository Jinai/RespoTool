# -*- coding: utf-8 -*-
# !python3

import os
import sys
import logging
import argparse
from logging.handlers import TimedRotatingFileHandler

LOG_LEVEL_STRINGS = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']


def init_logging(dirname, filename):
    log_dir = os.path.join(os.path.expanduser("~/Documents/"), dirname)
    try:
        os.makedirs(log_dir)
    except OSError:
        pass  # Directory already exists

    log_level = get_log_level()
    logger = logging.getLogger()
    logger.setLevel(log_level)
    fmt = logging.Formatter(fmt="{asctime} :: {levelname:<5} :: {name} :: {message}", datefmt="%Y-%m-%d %H:%M:%S",
                            style="{")
    console_handler = logging.StreamHandler(sys.stdout)
    file_handler = TimedRotatingFileHandler(filename=os.path.join(log_dir, filename),
                                            when="midnight",
                                            encoding="utf-8")
    console_handler.setFormatter(fmt)
    file_handler.setFormatter(fmt)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return log_level


def get_log_level():
    parser = argparse.ArgumentParser(__name__)
    parser.add_argument('--log-level',
                        default='DEBUG',
                        dest='log_level',
                        type=log_level_string_to_int,
                        nargs='?',
                        help='Set the logging output level. {0}'.format(LOG_LEVEL_STRINGS))
    parsed_args = parser.parse_args()
    return parsed_args.log_level


def log_level_string_to_int(log_level_string):
    if not log_level_string in LOG_LEVEL_STRINGS:
        message = 'Invalid choice: {0} (choose from {1})'.format(log_level_string, LOG_LEVEL_STRINGS)
        raise argparse.ArgumentTypeError(message)

    log_level_int = getattr(logging, log_level_string, logging.INFO)
    # check the logging log_level_choices have not changed from our expected values
    assert isinstance(log_level_int, int)

    return log_level_int
