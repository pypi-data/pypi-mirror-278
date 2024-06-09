"""
Burin Filterer

Copyright (c) 2024 William Foster with BSD 3-Clause License
See included LICENSE file for details.

This module has some portions based on the Python standard logging library
which is under the following licenses:
Copyright (c) 2001-2024 Python Software Foundation; All Rights Reserved
Copyright (c) 2001-2022 Vinay Sajip. All Rights Reserved.
See included LICENSE file for details.
"""

from .._log_records import BurinLogRecord

class BurinFilterer:
    """
    A base class for loggers and handlers to allow common code for filtering.

    .. note::

        This works identically to the :class:`logging.Filterer` in Python 3.12.
        The class is recreated in Burin to simplify allowing the
        :meth:`BurinFilterer.filter` method to return a log record.  This was
        added to the standard library in 3.12 and is supported here for all
        versions of Python compatible with Burin (including versions below
        3.12).
    """

    def __init__(self):
        """
        Initializes the filterer with an empty list of filters.
        """

        self.filters = []

    def add_filter(self, filter):  # noqa: A002
        """
        Adds the specified filter to the the list of filters.

        :param filter: The filter to add to this filterer instance.
        :type filter: BurinFilter
        """

        if filter not in self.filters:
            self.filters.append(filter)

    def filter(self, record):
        """
        Determine if a record is loggable according to all filters.

        All filters are checked in the order that they were added using the
        :meth:`BurinFilterer.add_filter` method.  If any filter returns
        **False** the record will not be logged.

        If a filter returns a log record instance then that instance will be
        used for all further processing.

        If none of the filters return **False** then a log record will be
        returned.  If any filters returned an instance of a log record then the
        returned record will be the last instance that was returned by a
        filter.

        However if any filter does return a **False** value then this method
        will also return a false value.

        .. note::

            In Python 3.12 the ability for a filterer to return a record was
            added to the standard library; it is supported here for all
            versions of Python compatible with Burin (including versions below
            3.12).

        :param record: The log record instance to check.
        :type record: BurinLogRecord
        :returns: An instance of the record if it should be logged or **False**
                  if it shouldn't.  If any filters modified the record or
                  returned an different instance of a record then that is what
                  will be returned here.  It should be used for all further
                  processing and handling of the log record event.
        :rtype: BurinLogRecord | bool
        """

        for eachFilter in self.filters:
            # Use the filter method if available, if not just use the filter
            # itself as a callable
            filterResult = eachFilter.filter(record) if hasattr(eachFilter, "filter") else eachFilter(record)

            # If any filter returns False then stop checking immediately
            if not filterResult:
                return False

            # If the filter returned a log record instance then use that
            if isinstance(filterResult, BurinLogRecord):
                record = filterResult

        # If no filter returned False then return the record instance we have
        return record

    def remove_filter(self, filter):  # noqa: A002
        """
        Removes the specified filter from the list of filters

        :param filter: The filter to remove from this filterer instance.
        :type filter: BurinFilter
        """

        if filter in self.filters:
            self.filters.remove(filter)

    # Aliases for better compatibility to replace standard library logging
    addFilter = add_filter
    removeFilter = remove_filter
