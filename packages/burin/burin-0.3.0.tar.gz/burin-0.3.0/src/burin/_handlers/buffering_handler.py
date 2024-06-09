"""
Burin Buffering Handler

Copyright (c) 2022-2024 William Foster with BSD 3-Clause License
See included LICENSE file for details.
"""

# Burin imports
from .handler import BurinHandler


class BurinBufferingHandler(BurinHandler):
    """
    A handler that stores log records in a buffer.

    Each time a record is added to the buffer a check is done to see if the
    buffer should be flushed.

    This class is intended to be subclassed by other handlers that need to use
    a buffering pattern and should not be instantiated directly except within a
    subclass *__init__* method.
    """

    def __init__(self, capacity, level="NOTSET"):
        """
        The buffer will flush once *capacity* number of records are stored.

        :param capacity: The number of log records to hold in the buffer before
                         flushing.
        :type capacity: int
        :param level: The logging level of the handler.  (Default = 'NOTSET')
        :type level: int | str
        """

        BurinHandler.__init__(self, level=level)
        self.capacity = capacity
        self.buffer = []

    def close(self):
        """
        Closes the handler and flush the buffer.
        """

        try:
            self.flush()
        finally:
            BurinHandler.close(self)

    def emit(self, record):
        """
        Emits a log record.

        This appends the record to the buffer.  Then this checks if the
        handler should flush, and if so flushes.

        :param record: The log record to emit.
        :type record: BurinLogRecord
        """

        self.buffer.append(record)

        if self.should_flush(record):
            self.flush()

    def flush(self):
        """
        Flushes the handler's buffer.

        This should be overridden in subclasses to customise the flushing
        behaviour.
        """

        with self.lock:
            self.buffer.clear()

    def should_flush(self, record): # noqa: ARG002
        """
        Checks if the handler should flush its buffer.

        This will simply return whether the buffer is currently at or above
        capacity.  This can be overridden in subclasses to perform other
        checks including ones that may use the provided *record* to make a
        determination.

        :param record: The log record being handled.  This is not used in this
                       base class method.
        :type record: BurinLogRecord
        :returns: Whether the handler should flush its buffer.
        :rtype: bool
        """

        return len(self.buffer) >= self.capacity

    # Aliases for better compatibility to replace standard library logging
    shouldFlush = should_flush
