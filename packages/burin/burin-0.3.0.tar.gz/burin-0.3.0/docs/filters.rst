.. currentmodule:: burin

=====================
Filters and Filterers
=====================

Filters can be used to determine if specific log records should be logged or
not, and also provide the ability to modify records during processing.

Both :class:`BurinLogger` and :class:`BurinHandler` are subclasses of
:class:`BurinFilterer`.  When processing a logging event all filter checks
will be done on the record to determine if it should be logged.

Custom filters can be created by subclassing :class:`BurinFilter` and
overriding the :meth:`BurinFilter.filter` method to perform custom checks or
modify log records in place during processing.

-----------
BurinFilter
-----------

The default :class:`BurinFilter` is based on :class:`logging.Filter` and
should function identically to it; it is not a subclass of it though.

.. autoclass:: BurinFilter
    :members: filter

-------------
BurinFilterer
-------------

This is a base class that is subclassed by both :class:`BurinLogger` and
:class:`BurinHandler` so that filtering functionality can be re-used in both.

While this is based on the standard library :class:`logging.Filterer` it is not
a subclass of it.

.. note::

    All methods of the :class:`BurinFilterer` with an *underscore_separated*
    name also have a *camelCase* alias name which matches the names used in the
    standard :mod:`logging` library.

.. autoclass:: BurinFilterer
    :members: add_filter, filter, remove_filter
