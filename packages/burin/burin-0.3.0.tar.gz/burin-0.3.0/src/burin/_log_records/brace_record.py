"""
Burin Brace Log Record

Copyright (c) 2022-2024 William Foster with BSD 3-Clause License
See included LICENSE file for details.
"""

# Python imports
import collections

# Burin imports
from .log_record import BurinLogRecord


class BurinBraceLogRecord(BurinLogRecord):
    """
    A log record that will be formatted in :meth:`str.format` ({ style).

    This allows for deferred formatting using positional and/or keyword
    arguments that are passed in during log record creation.

    This is derived from :class:`BurinLogRecord`.
    """

    def get_message(self):
        """
        This formats the log message.

        All additional *args* and *kwargs* that were part of the log record
        creation are used for the formatting of the log message.

        :returns: The formatted log message.
        :rtype: str
        """

        msg = str(self.msg)
        # Handle if only a single dictionary was passed in as an arugment,
        # if not then self.args is a tuple
        if isinstance(self.args, collections.abc.Mapping):
            msg = msg.format(**self.args)
        elif self.args or self.kwargs:
            msg = msg.format(*self.args, **self.kwargs)
        return msg

    # Aliases for better compatibility to replace standard library logging
    getMessage = get_message
