"""
Burin Loggers and Manager

Copyright (c) 2022-2024 William Foster with BSD 3-Clause License
See included LICENSE file for details.
"""

# Package contents
from .logger import BurinLogger, get_logger, getLogger, root
from .logger_adapter import BurinLoggerAdapter
from ._manager import _BurinManager


# Initialize the logger manager and set it on the class
BurinLogger.manager = _BurinManager(root)

# Create the general functions for the getting and setting the logger class
def get_logger_class():
    """
    Gets the class that is used when instantiating new loggers.

    :returns: The class new loggers are created with.
    :rtype: BurinLogger
    """

    return BurinLogger.manager.loggerClass

def set_logger_class(newClass):
    """
    Sets a class to be used when instantiating new loggers.

    The class being set must be derived from :class:`BurinLogger`.

    :param newClass: A new class to be used when instantiating new loggers.
                     This must be a subclass of :class:`BurinLogger`.
    :type newClass: BurinLogger
    :raises TypeError: If the received class is not a subclass of
                       :class:`BurinLogger`.
    """

    BurinLogger.manager.loggerClass = newClass

# Aliases for better compatibility to replace standard library logging
getLoggerClass = get_logger_class
setLoggerClass = set_logger_class


__all__ = ["BurinLogger", "get_logger", "getLogger", "root",
           "BurinLoggerAdapter", "get_logger_class", "getLoggerClass",
           "set_logger_class", "setLoggerClass"]
