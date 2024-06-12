"""This is the standard logger used in Kasheesh infrastructure.
"""

import logging


def get_my_logger(name="foo", level=logging.INFO):
    fmt = "[%(levelname)s %(asctime)s]:[%(filename)s:%(lineno)s]-%(funcName)2s(): %(message)s"
    logging.basicConfig(format=fmt, datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger(f"logger_{name}")
    logger.setLevel(level)
    return logger


