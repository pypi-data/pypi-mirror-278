"""
Burin Filter

Copyright (c) 2024 William Foster with BSD 3-Clause License
See included LICENSE file for details.

This module has some portions based on the Python standard logging library
which is under the following licenses:
Copyright (c) 2001-2024 Python Software Foundation; All Rights Reserved
Copyright (c) 2001-2022 Vinay Sajip. All Rights Reserved.
See included LICENSE file for details.
"""

class BurinFilter:
    """
    A filter can be used to apply filtering or modification of log records.

    .. note::

        This functions identically to the standard library
        :class:`logging.Filter` class.

    The base filter by default will allow all events which are lower in the
    logger hierarchy.
    """

    def __init__(self, name=""):
        """
        This creates the filter for the specified name.

        The name of logger is used to allow only events from the specified
        logger and all loggers lower in the hierarchy.  If this is an empty
        string the all events are allowed.

        :param name: The name of the logger to allow events from along with all
                     other loggers lower in the hierarchy.  All events are
                     allowed if this is an empty string.  (Default = '')
        :type name: str
        """

        self.name = name
        self.nameLength = len(name)

    def filter(self, record):
        """
        Determines if the record should be logged.

        .. note::

            If you are subclassing :class:`BurinFilter` and intend to modify
            the log record then the modified record should also be returned.
            The :class:`BurinFilterer` will then use the modified record
            for all further processing and return it to the original caller.

        :param record: The record to check.
        :type record: BurinLogRecord
        :returns: Whether the record should be logged or not.
        :rtype: bool
        """

        if self.nameLength == 0 or (self.name == record.name):
            return True

        if not record.name.startswith(self.name):
            return False

        return record.name[self.nameLength] == "."
