"""
Burin Log Record

Copyright (c) 2022-2024 William Foster with BSD 3-Clause License
See included LICENSE file for details.

This module has some portions based on the Python standard logging library
which is under the following licenses:
Copyright (c) 2001-2024 Python Software Foundation; All Rights Reserved
Copyright (c) 2001-2022 Vinay Sajip. All Rights Reserved.
See included LICENSE file for details.
"""

# Python imports
import collections
import os
import threading
import time
import sys

# Burin Imports
from .._log_levels import get_level_name
from .._state import config, _internals


class BurinLogRecord:
    """
    Represents all of the values of a logging event.

    .. note::

        Unlike the builtin :class:`logging.LogRecord` this does not perform any
        formatting of the log message.  It is instead intended to just be a
        base class to be inherited from.

        The :class:`BurinPercentLogRecord` instead provides the same printf (%
        style) formatting of the Python builtin LogRecord.

    .. note::

        In Python 3.12 the *taskName* attribute was added to the standard
        :class:`logging.LogRecord` class; it is supported here for all
        versions of Python compatible with Burin (including versions below
        3.12).

        However; names were added to :class:`asyncio.Task` objects in Python
        3.8, so in Python 3.7 the *taskName* attribute on a log record will
        always be **None**.

    Custom log record factories that are created should inherit from this and
    typically only override the :meth:`BurinLogRecord.get_message` method.
    """

    #: This is the key used for the class as a log record factory.  This is
    #: updated automatically when the class is set using
    #: :func:`set_log_record_factory`.
    factoryKey = None

    def __init__(self, name, level, pathname, lineno, msg, args, exc_info,  # noqa: C901 PLR0912 PLR0915
                 func=None, sinfo=None, **kwargs):
        """
        This initializes the log record and stores all relevant values.

        Unlike the standard library :class:`logging.LogRecord` this also stores
        all extra *kwargs* that were not used in the logging call.   These can
        then be used later when formatting the log message.

        :param name: The name of the logger that was called.
        :type name: str
        :param level: The level for the log message.
        :type level: int
        :param pathname: The full pathname of the file where the logging call
                         was made.
        :type pathname: str
        :param lineno: The line number of where the logging call was made.
        :type lineno: int
        :param msg: The logging message.
        :type msg: str
        :param args: Additional positional arguments passed with the logging
                     call.
        :type args: tuple(Any) | None
        :param exc_info: Exception information related to the logging call.
        :type exc_info: tuple(type, Exception, traceback)
        :param func: The name of the function where the logging call was made.
        :type func: str
        :param sinfo: Text of the stack information from where the logging call
                      was made.
        :type sinfo: str
        """

        # Get the time the record is created
        recordTime = time.time()

        self.name = name
        self.msg = msg

        # This is to allow the passing of a dictionary as a sole argument to
        # allow for things like:
        #     burin.debug("a %(a)d b %(b)s", {'a': 1, 'b':2})
        # This is a feature of the Python standard library's LogRecord class
        # and is duplicated here (from Python 3.12.2) to provide a proper
        # replacement for as many use cases as possible
        if (args and len(args) == 1 and isinstance(args[0], collections.abc.Mapping) and args[0]):
            args = args[0]

        self.args = args
        self.kwargs = kwargs
        self.levelname = get_level_name(level)
        self.levelno = level
        self.exc_info = exc_info
        self.exc_text = None    # Used by BurinFormatter to cache traceback text
        self.stack_info = sinfo
        self.lineno = lineno
        self.funcName = func
        self.created = recordTime
        self.msecs = int((recordTime - int(recordTime)) * 1000) + 0.0   # See CPython gh-89047
        self.relativeCreated = (self.created - _internals["startTime"]) * 1000

        self.pathname = pathname
        try:
            self.filename = os.path.basename(pathname)
            self.module = os.path.splitext(self.filename)[0]
        except (TypeError, ValueError, AttributeError):
            self.filename = pathname
            self.module = "Unknown module"

        if config.logThreads:
            self.thread = threading.get_ident()
            self.threadName = threading.current_thread().name
        else:
            self.thread = None
            self.threadName = None

        if config.logMultiprocessing:
            self.processName = "MainProcess"
            multiProcessing = sys.modules.get("multiprocessing")
            if multiProcessing is not None:
                try:
                    self.processName = multiProcessing.current_process().name
                except Exception:
                    pass
        else:
            self.processName = None

        if config.logProcesses and hasattr(os, "getpid"):
            self.process = os.getpid()
        else:
            self.process = None

        self.taskName = None
        if config.logAsyncioTasks:
            asyncio = sys.modules.get("asyncio")
            if asyncio:
                try:
                    self.taskName = asyncio.current_task().get_name()
                except Exception:
                    pass

    def get_message(self):
        """
        This returns the log message.

        This should be overridden in subclasses to provide additional
        formatting or other modifications to the log message.

        :returns: The log message.
        :rtype: str
        """

        return str(self.msg)

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.name}, {self.levelno}, {self.pathname}, {self.lineno}, {self.msg}>"

    # Aliases for better compatibility to replace standard library logging
    getMessage = get_message
