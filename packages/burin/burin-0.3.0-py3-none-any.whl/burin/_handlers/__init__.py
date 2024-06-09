"""
Burin Handlers

Copyright (c) 2022-2024 William Foster with BSD 3-Clause License
See included LICENSE file for details.
"""

# Python imports
from logging.handlers import (DEFAULT_HTTP_LOGGING_PORT, DEFAULT_SOAP_LOGGING_PORT,
                              DEFAULT_TCP_LOGGING_PORT, DEFAULT_UDP_LOGGING_PORT,
                              SYSLOG_TCP_PORT, SYSLOG_UDP_PORT)

# Burin imports
from .._log_levels import WARNING

# Package contents
from .base_rotating_handler import BurinBaseRotatingHandler
from .buffering_handler import BurinBufferingHandler
from .datagram_handler import BurinDatagramHandler
from .file_handler import BurinFileHandler
from .handler import BurinHandler
from .http_handler import BurinHTTPHandler
from .memory_handler import BurinMemoryHandler
from .nt_event_log_handler import BurinNTEventLogHandler
from .null_handler import BurinNullHandler
from .queue_handler import BurinQueueHandler
from .queue_listener import BurinQueueListener
from .rotating_file_handler import BurinRotatingFileHandler
from .smtp_handler import BurinSMTPHandler
from .socket_handler import BurinSocketHandler
from .stream_handler import BurinStreamHandler
from .syslog_handler import BurinSyslogHandler
from .timed_rotating_file_handler import BurinTimedRotatingFileHandler
from .watched_file_handler import BurinWatchedFileHandler
from ._references import _handlers, _handlerList
from ._stderr_handler import _BurinStderrHandler


# The last resort if no other handlers are set
lastResort = _BurinStderrHandler(WARNING)

def get_handler_by_name(name):
    """
    Gets a handler with the specified name.

    If no handler exists with the name then **None** is returned.

    :param name: The name of the handler to get.
    :type name: str
    :returns: The handler with the specified name or **None** if it doesn't
              exist.
    :rtype: BurinHandler | None
    """

    return _handlers.get(name)

def get_handler_names():
    """
    Gets all known handler names as an immutable set.

    :returns: A frozenset of the handler names.
    :rtype: frozenset
    """

    return frozenset(set(_handlers.keys()))

# Aliases for better compatibility to replace standard library logging
getHandlerByName = get_handler_by_name
getHandlerNames = get_handler_names


__all__ = ["DEFAULT_HTTP_LOGGING_PORT", "DEFAULT_SOAP_LOGGING_PORT",
           "DEFAULT_TCP_LOGGING_PORT", "DEFAULT_UDP_LOGGING_PORT",
           "SYSLOG_TCP_PORT", "SYSLOG_UDP_PORT", "BurinBaseRotatingHandler",
           "BurinBufferingHandler", "BurinDatagramHandler", "BurinFileHandler",
           "BurinHandler", "BurinHTTPHandler", "BurinMemoryHandler",
           "BurinNTEventLogHandler", "BurinNullHandler", "BurinQueueHandler",
           "BurinQueueListener", "BurinRotatingFileHandler", "BurinSMTPHandler",
           "BurinSocketHandler", "BurinStreamHandler", "BurinSyslogHandler",
           "BurinTimedRotatingFileHandler", "BurinWatchedFileHandler",
           "lastResort", "get_handler_by_name", "getHandlerByName",
           "get_handler_names", "getHandlerNames"]


# Clean up some things that aren't part of this package
del WARNING
