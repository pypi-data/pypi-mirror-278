"""
Burin Stream Handler

Copyright (c) 2022-2024 William Foster with BSD 3-Clause License
See included LICENSE file for details.

This module has some portions based on the Python standard logging library
which is under the following licenses:
Copyright (c) 2001-2024 Python Software Foundation; All Rights Reserved
Copyright (c) 2001-2022 Vinay Sajip. All Rights Reserved.
See included LICENSE file for details.
"""

# Python imports
import sys

# Burin imports
from .._log_levels import get_level_name
from .handler import BurinHandler


class BurinStreamHandler(BurinHandler):
    """
    A handler that writes log records to a stream.

    .. note::

        This handler will not close the stream it is writing to as
        :obj:`sys.stdout` and :obj:`sys.stderr` are commonly used.
    """

    terminator = "\n"

    def __init__(self, stream=None, level="NOTSET"):
        """
        This initializes the handler and sets the *stream* to use.

        If *stream* is **None** then :obj:`sys.stderr` is used by default.

        :param stream: The stream to log to.  If this is **None** then
                       :obj:`sys.stderr` is used.
        :type stream: io.TextIOBase
        :param level: The logging level of the handler.  (Default = 'NOTSET')
        :type level: int | str
        """

        BurinHandler.__init__(self, level=level)
        if stream is None:
            stream = sys.stderr
        self.stream = stream

    def emit(self, record):
        r"""
        Emits a log record.

        This will format and then write the record to the stream with a
        trailing newline.  The newline character is whatever the
        :attr:`BurinStreamHandler.terminator` property is set to (default
        ``\n``).

        :param record: The log record to emit.
        :type record: BurinLogRecord
        :raises RecursionError: This is to prevent an interpreter crash if a
                                recursion error is raised.  See Python #36272
        """

        try:
            msg = self.format(record)
            self.stream.write(f"{msg}{self.terminator}")
            self.flush()
        except RecursionError: # Python issue 36272
            raise
        except Exception:
            self.handle_error(record)

    def flush(self):
        """
        Flushes the stream.
        """

        with self.lock:
            if self.stream and hasattr(self.stream, "flush"):
                self.stream.flush()

    def set_stream(self, stream):
        """
        Sets the stream for the handler to write to.

        This will return the previous stream if the stream has changed, or
        **None** if the new stream is the same or there was no previous stream.

        .. note::

            This will flush the previous stream before assigning the new one.

        :param stream: The stream the handler will write to.
        :type stream: io.TextIOBase
        :returns: The previous stream or **None** if both streams are the same
                  or there was no previous stream.
        :rtype: io.TextIOBase | None
        """

        if stream is self.stream:
            oldStream = None
        else:
            oldStream = self.stream

            with self.lock:
                self.flush()
                self.stream = stream

        return oldStream

    # Aliases for better compatibility to replace standard library logging
    setStream = set_stream

    def __repr__(self):
        level = get_level_name(self.level)
        name = getattr(self.stream, "name", "")

        # Name could be an int
        name = str(name)
        if name:
            name += " "

        return f"<{self.__class__.__name__} {name}({level})>"
