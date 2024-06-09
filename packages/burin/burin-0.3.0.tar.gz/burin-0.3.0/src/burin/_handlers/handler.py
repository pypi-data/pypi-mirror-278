"""
Burin Base Handler

Copyright (c) 2024 William Foster with BSD 3-Clause License
See included LICENSE file for details.

This module has some portions based on the Python standard logging library
which is under the following licenses:
Copyright (c) 2001-2024 Python Software Foundation; All Rights Reserved
Copyright (c) 2001-2022 Vinay Sajip. All Rights Reserved.
See included LICENSE file for details.
"""

# Python Imports
from threading import RLock
import os.path
import sys
import traceback

# Burin Imports
from .._filters import BurinFilterer
from .._formatters import _defaultFormatter
from .._log_levels import get_level_name, _check_level
from .._log_records import BurinLogRecord
from .._state import config, _internals
from .._threading import _BurinLock, _register_at_fork_reinit_lock
from ._references import _add_handler_ref, _handlers


class BurinHandler(BurinFilterer):
    """
    Handlers emit logging events to specific destinations.

    .. note::

        This functions almost identically to :class:`logging.Handler` but has
        some minor changes that allow it to work within Burin.  These changes
        shouldn't impact normal usage when compared with the standard
        :mod:`logging` library.

        This is not a subclass of :class:`logging.Handler` and is not usable
        with the standard library :mod:`logging` module.

    This is the base handler class for Burin and should not be used directly,
    but instead can be subclassed to create other handlers that work with
    Burin.
    """

    def __init__(self, level="NOTSET"):
        """
        This will setup the basic instance values for the handler.

        Typically this should be called within any subclasses *__init__* method
        to ensure all required handler instance attributes are created.

        :param level: The logging level of the handler.  (Default = 'NOTSET')
        :type level: int | str
        """

        BurinFilterer.__init__(self)
        self._name = None
        self.level = _check_level(level)
        self.formatter = None
        self._closed = False
        _add_handler_ref(self)
        self.create_lock()

    # This property is supported by two methods in the standard library Handler
    # called get_name and set_name.  It is simplified here to just the property
    # as the methods are not documented in the standard library
    @property
    def name(self):
        """
        The name of the handler.
        """
        return self._name

    @name.setter
    def name(self, name):
        with _BurinLock:
            if self._name in _handlers:
                del _handlers[self._name]

            self._name = name

            if name:
                _handlers[name] = self

    def acquire(self):
        """
        Acquires the handlers internal thread lock.

        It is recommended to use a handler's lock in a context manager using
        the **with** statement.  The lock is simply accessible as
        :attr:`BurinHandler.lock` on any handler instance.

        The :meth:`BurinHandler.acquire` and :meth:`BurinHandler.release`
        methods are primarily provided for improved compatibility with the
        standard library :class:`logging.Handler`.
        """

        if self.lock:
            self.lock.acquire()

    def close(self):
        """
        Cleans up the handler.

        This simply removes the handler from an internal library reference map,
        but any subclasses should ensure this is called in any overridden
        *close()* methods to ensure the reference to the handler is cleaned up.
        """

        with _BurinLock:
            self._closed = True
            if self._name and self._name in _handlers:
                del _handlers[self._name]

    def create_lock(self):
        """
        Creates a re-entrant lock for the handler for threading protection.

        The lock is available through the instance :attr:`BurinHandler.lock`
        attribute or it can be used with :meth:`BurinHandler.acquire` and
        :meth:`BurinHandler.release`.

        This lock can then be used by subclasses to serialize access to I/O or
        any other places where protection of the instance across threads may be
        needed.

        This also registers the handler to reinitialize the lock after a fork
        as otherwise it could prevent logging through the handler if fork is
        called while the lock is held.
        """

        self.lock = RLock()
        _register_at_fork_reinit_lock(self)

    def emit(self, record):
        """
        Should do whatever is need to actually log the specified record.

        This should be implemented within a subclass and will only raise a
        :exc:`NotImplementedError` in this base class.

        :raises NotImplementedError: As this is not implemented in the base
                                     class.
        """

        raise NotImplementedError("emit must be implemented by BurinHandler "
                                  "subclasses")

    def flush(self):
        """
        Meant to ensure that all logging output is flushed.

        This is intended to be implemented within subclasses as needed; this
        method on the base class does not do anything.
        """
        pass

    def format(self, record):
        """
        Formats the received log record.

        If the handler doesn't have a formatter a basic default formatter is
        used.

        :param record: The log record to be formatted.
        :type record: BurinLogRecord
        :returns: The formatted text of the log record.
        :rtype: str
        """

        fmt = self.formatter if self.formatter is not None else _defaultFormatter

        return fmt.format(record)

    def handle(self, record):
        """
        Process the log record and possibly emit it.

        This will check any filters that have been added to the handler and
        emit the record if no filters return **False**.

        If the record passes all filters then the instance of the record that
        was emitted will be returned.

        .. note::

            In Python 3.12 the ability for this to return a record was added to
            the standard library; it is supported here for all versions of
            Python compatible with Burin (including versions below 3.12).

        :param record: The log record to process.
        :type record: BurinLogRecord
        :returns: An instance of the record that was emitted, or **False** if
                  the record was not emitted.
        :rtype: BurinLogRecord | bool
        """

        filterResult = self.filter(record)

        if not filterResult:
            return False

        if isinstance(filterResult, BurinLogRecord):
            record = filterResult

        with self.lock:
            self.emit(record)

        return record

    def handle_error(self, record):
        """
        Handles errors which may occur during an *emit()* call.

        This should be called from subclasses when an exception is encountered
        during an *emit()* call.

        If :attr:`raiseExceptions` is **False** then the error will be
        silently ignored.  This can be useful for a logging system as most
        users would be more concerned with application errors vs logging
        library errors.

        However if :attr:`raiseExceptions` is **True** then information about
        the error will be output to :obj:`sys.stderr`.

        :param record: The log record that was being processed when the error
                       occurred.
        :type record: BurinLogRecord
        """

        if config.raiseExceptions and sys.stderr:  # Python issue 13807
            excType, excValue, excTrace = sys.exc_info()
            try:
                sys.stderr.write("--- Burin Logging error ---\n")
                traceback.print_exception(excType, excValue, excTrace, None,
                                          sys.stderr)
                sys.stderr.write("Call stack:\n")

                # Walk the stack frame up until we're out of Burin
                frame = excTrace.tb_frame
                srcDir = _internals["srcDir"]
                while hasattr(frame, "f_code"):
                    if frame and srcDir in os.path.normcase(frame.f_code.co_filename):
                        frame = frame.f_back
                    else:
                        break

                if frame:
                    traceback.print_stack(frame, file=sys.stderr)
                else:
                    sys.stderr.write(f"Logged from file {record.filename}, line "
                                     f"{record.lineno}")

                try:
                    sys.stderr.write(f"Message: {record.msg}\nArguments: "
                                     f"{record.args}\nKeyword Arguments: "
                                     f"{record.kwargs}\n")
                except RecursionError:  # Python issue 36272
                    raise
            except Exception:
                sys.stderr.write("Unable to print the message and arguments "
                                 "- possible formatting error.\nUse the "
                                 "traceback above to help find the error.\n")
            except OSError:
                pass  # Python issue 5971
            finally:
                del excType, excValue, excTrace

    def release(self):
        """
        Releases the handler's internal thread lock.

        It is recommended to use a handler's lock in a context manager using
        the **with** statement.  The lock is simply accessible as
        :attr:`BurinHandler.lock` on any handler instance.

        The :meth:`BurinHandler.acquire` and :meth:`BurinHandler.release`
        methods are primarily provided for improved compatibility with the
        standard library :class:`logging.Handler`.
        """

        if self.lock:
            self.lock.release()

    def set_formatter(self, fmt):
        """
        Sets the formatter to be used by this handler.

        :param fmt: The formatter to use.
        :type fmt: BurinFormatter
        """

        self.formatter = fmt

    def set_level(self, level):
        """
        Sets the logging level of this handler.

        :param level: The new level for the handler.
        :type level: int | str
        """

        self.level = _check_level(level)

    def _at_fork_reinit(self):
        """
        Attempts to reinitialize the internal lock after a fork.
        """
        try:
            self.lock._at_fork_reinit()
        except AttributeError:
            pass

    def __repr__(self):
        level = get_level_name(self.level)
        return f"<{self.__class__.__name__} ({level})>"

    # Aliases to override standard library handler
    createLock = create_lock
    handleError = handle_error
    setFormatter = set_formatter
    setLevel = set_level
