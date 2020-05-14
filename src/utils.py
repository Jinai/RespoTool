# -*- coding: utf-8 -*-
# !python3

import argparse
import inspect
import logging
import os
import re
import sys
from logging.handlers import TimedRotatingFileHandler

import urlmarker
from _meta import __appname__, __version__


def resource_path(relative_path):
    working_directory = "."
    if hasattr(sys, "frozen") and hasattr(sys, "_MEIPASS"):
        working_directory = sys._MEIPASS
    return os.path.join(working_directory, os.path.normpath(relative_path))


def init_logging(file=True):
    log_level = get_log_level()
    logger = logging.getLogger()
    logger.setLevel(log_level)
    fmt = "{asctime}.{msecs:03.0f} :: {levelname:<5} :: {name:<9} :: {message}"
    datefmt = "%d/%m/%Y %H:%M:%S"
    fmt = logging.Formatter(fmt=fmt, datefmt=datefmt, style="{")
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(fmt)
    logger.addHandler(console_handler)

    if file and hasattr(sys, "frozen"):
        log_dir = os.path.join(os.path.expanduser(os.path.join("~", "Documents")), __appname__)
        created_log_dir = create_directory(log_dir)

        path = os.path.join(log_dir, __appname__.lower() + ".log")
        file_handler = TimedRotatingFileHandler(filename=path, when="midnight", encoding="utf-8")
        file_handler.setFormatter(fmt)
        logger.addHandler(file_handler)
        if created_log_dir:
            logger.info("Creating '{}'".format(log_dir))
    return logging._levelToName[log_level]


def create_directory(dirname):
    try:
        os.makedirs(dirname)
        return True
    except OSError:
        return False


def get_log_level():
    choices = [key for key in logging._levelToName.values()][-2::-1]
    help_string = "set the logging output level to {0}".format(special_join(choices, ", ", " or "))
    parser = argparse.ArgumentParser(__appname__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-v", "--version", action="version",
                        version="%(prog)s {}".format(__version__), help="show the version number and exit")
    parser.add_argument("--log",
                        default=logging._levelToName[logging.DEBUG],
                        dest="log_level",
                        type=lambda arg: logging._checkLevel(arg.upper()),
                        nargs="?",
                        help=help_string)
    parsed_args = parser.parse_args()
    return parsed_args.log_level


def log_args(logger=None):
    def wrap(func):
        # Unpack function's arg count, arg names, arg defaults
        code = func.__code__
        argcount = code.co_argcount
        argnames = code.co_varnames[:argcount]
        defaults = func.__defaults__ or list()
        argdefs = dict(zip(argnames[-len(defaults):], defaults))

        def wrapped(*v, **k):
            # Collect function arguments by chaining together positional,
            # defaulted, extra positional and keyword arguments.
            positional = [format_arg_value((arg, val)) for arg, val in zip(argnames, v) if arg != "self"]
            defaulted = [format_arg_value((a, argdefs[a])) for a in argnames[len(v):] if a not in k]
            nameless = [repr(arg) for arg in v[argcount:]]
            keyword = [format_arg_value(item) for item in k.items()]
            args = positional + defaulted + nameless + keyword
            loggr = logger
            if loggr is None:
                loggr = logging.getLogger()
            loggr.debug("{}({}) called by {}.{}()".format(func.__name__, ", ".join(args),
                                                          inspect.stack()[1][0].f_locals["self"].__class__.__name__,
                                                          inspect.stack()[1][3]))
            return func(*v, **k)

        return wrapped

    return wrap


def format_arg_value(arg_val):
    arg, val = arg_val
    return "{}={!r}".format(arg, val)


def validate_indexes(indexes):
    for pos, idx in enumerate(indexes):
        if pos != idx:
            return False
    return len(indexes)


def text_ellipsis(text, *, width, placeholder="..."):
    if not isinstance(text, str) or width < len(placeholder):
        raise ValueError
    if len(text) <= width:
        return text
    return text[:width - len(placeholder)] + placeholder


def extract_urls(text):
    return re.findall(urlmarker.URL_REGEX, text)


def extract_numbers(text):
    return re.findall("\d+", text)


def sequence_chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))


def special_join(seq, sep, last_sep):
    result = ""
    if len(seq) == 0:
        return result
    elif len(seq) == 1:
        return str(seq[0])
    for index, elem in enumerate(seq):
        result += elem
        if index < len(seq) - 2:
            result += sep
        elif index == len(seq) - 2:
            result += last_sep

    return result
