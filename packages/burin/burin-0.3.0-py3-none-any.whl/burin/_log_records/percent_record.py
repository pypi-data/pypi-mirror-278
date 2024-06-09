"""
Burin Percent Log Record

Copyright (c) 2022 William Foster with BSD 3-Clause License
See included LICENSE file for details.
"""

# Burin imports
from .log_record import BurinLogRecord


class BurinPercentLogRecord(BurinLogRecord):
    """
    A log record that will be formatted like printf (% style).

    This allows for deferred formatting using positional arguments that are
    passed in during log record creation.

    This should behave identically to the Python builtin
    :class:`logging.LogRecord` in normal use cases.

    This is derived from :class:`BurinLogRecord`.
    """

    def get_message(self):
        """
        This formats the log message.

        All additional *args* that were part of the log record creation are
        used for the formatting of the log message.

        :returns: The formatted log message.
        :rtype: str
        """

        msg = str(self.msg)
        if self.args:
            msg = msg % self.args
        return msg

    # Aliases for better compatibility to replace standard library logging
    getMessage = get_message
