.. currentmodule:: burin

===========
Log Records
===========

A log record represents a logging event and all of the values associated with
that event.

When a logger is processing a logging event it will create a new log record,
the class used for creating the record is referred to as a log record factory.

Unlike the standard :mod:`logging` package Burin allows for multiple log record
factories to be set at once.  The factory that is used can be set on a per
logger basis using the :attr:`BurinLogger.msgStyle` property; this should be
the ``factoryKey`` of the record.

The built-in log record factories for Burin are focused on allowing different
styles of deferred formatting which is demonstrated in the
:ref:`intro:Deferred Formatting Styles` section.

Custom log record factories can be added though and offer a lot flexibility in
how a log message is processed.  An example of this is demonstrated in the
:ref:`intro:Customisable Log Records` section.

.. note::

    Only methods defined within each Burin log record class are documented
    here. All log records inherit from the :class:`BurinLogRecord` class.

    All methods of the log record classes with an *underscore_separated* name
    also have a *camelCase* alias name which matches the names used in the
    standard :mod:`logging` library.

--------------
BurinLogRecord
--------------

This is the base log record; and is not used as a log record factory.  It is
meant to be subclassed by other log records.  No formatting is done to the
message.

All other Burin log record classes are derived from this class.

.. autoclass:: BurinLogRecord
    :members: get_message

-------------------
BurinBraceLogRecord
-------------------

This log record can be used for :meth:`str.format` style formatting.

.. autoclass:: BurinBraceLogRecord
    :class-doc-from: class
    :members: get_message

    .. autoattribute:: factoryKey

--------------------
BurinDollarLogRecord
--------------------

This log record can be used for :class:`string.Template` style formatting.

.. autoclass:: BurinDollarLogRecord
    :class-doc-from: class
    :members: get_message

    .. autoattribute:: factoryKey

---------------------
BurinPercentLogRecord
---------------------

This is the default log record factory and uses printf style formatting.

This should behave identically to :class:`logging.LogRecord`.

.. autoclass:: BurinPercentLogRecord
    :class-doc-from: class
    :members: get_message

    .. autoattribute:: factoryKey
