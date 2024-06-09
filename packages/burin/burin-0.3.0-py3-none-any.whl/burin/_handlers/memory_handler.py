"""
Burin Memory Handler

Copyright (c) 2022-2024 William Foster with BSD 3-Clause License
See included LICENSE file for details.

This module has some portions based on the Python standard logging library
which is under the following licenses:
Copyright (c) 2001-2024 Python Software Foundation; All Rights Reserved
Copyright (c) 2001-2022 Vinay Sajip. All Rights Reserved.
See included LICENSE file for details.
"""

# Burin imports
from .._log_levels import _check_level
from .buffering_handler import BurinBufferingHandler


class BurinMemoryHandler(BurinBufferingHandler):
    """
    A handler which buffers log records in memory.

    This is derived from :class:`BurinBufferingHandler`.

    This handler will flush when the buffer reaches the specified *capacity* or
    when a record of the specified *flushLevel* or above is emitted.
    """

    def __init__(self, capacity, flushLevel="ERROR", target=None,
                 flushOnClose=True, level="NOTSET"):
        """
        The *target* handler will be called when this flushes its buffer.

        :param capacity: The number of log records to hold in the buffer before
                         flushing.
        :type capacity: int
        :param flushLevel: If a log record of this level is put in the buffer
                           it will immediately flush the whole buffer.
                           (Default = 'ERROR')
        :type flushLevel: int | str
        :param target: The handler which is called with the log records when
                       the buffer is flushed.
        :type target: BurinHandler
        :param flushOnClose: Whether the buffer should be flushed when the
                             handler is closed.  (Default = **True**)
        :type flushOnClose: bool
        :param level: The logging level of the handler.  (Default = 'NOTSET')
        :type level: int | str
        """

        BurinBufferingHandler.__init__(self, capacity, level=level)
        self.flushLevel = _check_level(flushLevel)
        self.target = target
        self.flushOnClose = flushOnClose

    def close(self):
        """
        Closes the handler.

        This will also flush the buffer if *flushOnClose* was **True** when the
        handler was initialized.
        """

        try:
            if self.flushOnClose:
                self.flush()
        finally:
            with self.lock:
                self.target = None
                BurinBufferingHandler.close(self)

    def flush(self):
        """
        This sends the memory handler's buffered records to the target handler.

        If there is no current target handler this will not do anything.
        """

        with self.lock:
            if self.target is not None:
                for record in self.buffer:
                    self.target.handle(record)

                self.buffer.clear()

    def set_target(self, target):
        """
        Sets the target handler for this handler.

        :param target: The target handler to flush to when this handler's
                       buffer is full or should be flushed.
        :type target: BurinHandler
        """

        with self.lock:
            self.target = target

    def should_flush(self, record):
        """
        Checks the level and buffer size for if the buffer should be flushed.

        This will determine if the buffer should be flushed based on either the
        current size of the buffer and also the record level.

        :param record: The log record being handled.
        :type record: BurinLogRecord
        :returns: Whether the buffer should be flushed.
        :rtype: bool
        """

        return (len(self.buffer >= self.capacity)) or (record.levelno > self.flushLevel)

    # Aliases for better compatibility to replace standard library logging
    setTarget = set_target
    shouldFlush = should_flush
