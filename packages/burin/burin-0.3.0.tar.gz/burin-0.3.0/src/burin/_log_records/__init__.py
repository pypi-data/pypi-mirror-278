"""
Burin Loggers and Manager

Copyright (c) 2022 William Foster with BSD 3-Clause License
See included LICENSE file for details.
"""

# Package contents
from .brace_record import BurinBraceLogRecord
from .dollar_record import BurinDollarLogRecord
from .log_record import BurinLogRecord
from .percent_record import BurinPercentLogRecord


logRecordFactories = {}


def get_log_record_factory(msgStyle="%"):
    """
    Gets the log record factory class for the specified style.

    If no log record factory exists for the *msgStyle* then **None** is
    returned.

    :param msgStyle: The style to get the associated log record factory for.
                     (Default = '%')
    :type msgStyle: str
    :returns: The log record factory class associated with the *msgStyle* or
              **None** if no factory exists for that style.
    :rtype: BurinLogRecord | None
    """

    try:
        return logRecordFactories[msgStyle]
    except KeyError:
        return None

def make_log_record(recordDict, msgStyle="%"):
    """
    Creates a new log record from a dictionary.

    This is intended for rebuilding log records that were pickled and sent
    over a socket.

    Typically *msgStyle* won't matter here as the msg formatting is done before
    a record is pickled and sent.  It is provided as a parameter here for
    special use cases.

    :param recordDict: The dictionary of the log record attributes.
    :type recordDict: dict{str: Any}
    :param msgStyle: The *msgStyle* of which log record factory to use when
                     rebuilding the record.  (Default = '%')
    :type msgStyle: str
    :returns: The reconstructed log record.
    :rtype: BurinLogRecord
    """

    logRecord = logRecordFactories[msgStyle](None, None, "", 0, "", (), None)
    logRecord.__dict__.update(recordDict)

    return logRecord

def set_log_record_factory(factory, msgStyle="%"):
    """
    Sets the log record class to use as a factory.

    The factory can be set to any type of *msgStyle*.  If a factory is already
    set for that *msgStyle* it is replaced, otherwise the new factory is simply
    added without impacting the other factories.

    Once a factory has been set to a *msgStyle* then the same style  can be
    used as the *msgStyle* on loggers to use that specific log record factory.

    :param factory: The new log record class to use as a factory.  This should
                    be a subclass of :class:`BurinLogRecord`.
    :type factory: BurinLogRecord
    :param msgStyle: The style and key used to reference the factory for
                     loggers.  (Default = '%')
    :type msgStyle: str
    """

    logRecordFactories[msgStyle] = factory
    factory.factoryKey = msgStyle


# Aliases for better compatibility to replace standard library logging
getLogRecordFactory = get_log_record_factory
makeLogRecord = make_log_record
setLogRecordFactory = set_log_record_factory


# Set the factories for the built-in record types
set_log_record_factory(BurinPercentLogRecord, "%")
set_log_record_factory(BurinBraceLogRecord, "{")
set_log_record_factory(BurinDollarLogRecord, "$")


__all__ = ["BurinBraceLogRecord", "BurinDollarLogRecord", "BurinLogRecord",
           "BurinPercentLogRecord", "get_log_record_factory",
           "getLogRecordFactory", "make_log_record", "makeLogRecord",
           "set_log_record_factory", "setLogRecordFactory",
           "logRecordFactories"]
