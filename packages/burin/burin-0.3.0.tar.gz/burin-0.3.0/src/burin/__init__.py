"""
Burin Logging Package

Copyright (c) 2022-2024 William Foster with BSD 3-Clause License
See included LICENSE file for details.
"""

__author__ = "William Foster"
__license__ = "BSD-3-Clause"
__title__ = "Burin"
__version__ = "0.3.0"


# Package contents
from ._burin import (critical, debug, disable, error, exception, info, log,
                     shutdown, warning)
from ._config import basic_config, basicConfig
from ._exceptions import ConfigError, FactoryError, FormatError
from ._filters import BurinFilter, BurinFilterer
from ._formatters import BurinBufferingFormatter, BurinFormatter
from ._handlers import (BurinBaseRotatingHandler, BurinBufferingHandler,
                        BurinDatagramHandler, BurinFileHandler, BurinHandler,
                        BurinHTTPHandler, BurinMemoryHandler,
                        BurinNTEventLogHandler, BurinNullHandler,
                        BurinQueueHandler, BurinQueueListener,
                        BurinRotatingFileHandler, BurinSMTPHandler,
                        BurinSocketHandler, BurinStreamHandler,
                        BurinSyslogHandler, BurinTimedRotatingFileHandler,
                        BurinWatchedFileHandler, get_handler_by_name,
                        getHandlerByName, get_handler_names, getHandlerNames)
from ._log_levels import (CRITICAL, DEBUG, ERROR, INFO, NOTSET, WARNING,
                          get_level_name, getLevelName,
                          get_level_names_mapping, getLevelNamesMapping)
from ._log_records import (BurinBraceLogRecord, BurinDollarLogRecord,
                           BurinLogRecord, BurinPercentLogRecord,
                           get_log_record_factory, getLogRecordFactory,
                           make_log_record, makeLogRecord,
                           set_log_record_factory, setLogRecordFactory)
from ._loggers import (BurinLogger, BurinLoggerAdapter,
                       get_logger, getLogger, get_logger_class, getLoggerClass,
                       set_logger_class, setLoggerClass)
from ._state import config
from ._warnings import capture_warnings, captureWarnings


__all__ = ["critical", "debug", "disable", "error", "exception", "info", "log",
           "shutdown", "warning", "basic_config", "basicConfig", "ConfigError",
           "FactoryError", "FormatError", "BurinFilter", "BurinFilterer",
           "BurinBufferingFormatter", "BurinFormatter",
           "BurinBaseRotatingHandler", "BurinBufferingHandler",
           "BurinDatagramHandler", "BurinFileHandler", "BurinHandler",
           "BurinHTTPHandler", "BurinMemoryHandler", "BurinNTEventLogHandler",
           "BurinNullHandler", "BurinQueueHandler", "BurinQueueListener",
           "BurinRotatingFileHandler", "BurinSMTPHandler",
           "BurinSocketHandler", "BurinStreamHandler", "BurinSyslogHandler",
           "BurinTimedRotatingFileHandler", "BurinWatchedFileHandler",
           "get_handler_by_name", "getHandlerByName", "get_handler_names",
           "getHandlerNames", "CRITICAL", "DEBUG", "ERROR", "INFO", "NOTSET",
           "WARNING", "get_level_name", "getLevelName",
           "get_level_names_mapping", "getLevelNamesMapping",
           "BurinBraceLogRecord", "BurinDollarLogRecord", "BurinLogRecord",
           "BurinPercentLogRecord", "get_log_record_factory",
           "getLogRecordFactory", "make_log_record", "makeLogRecord",
           "set_log_record_factory", "setLogRecordFactory", "BurinLogger",
           "BurinLoggerAdapter", "get_logger", "getLogger", "get_logger_class",
           "getLoggerClass", "set_logger_class", "setLoggerClass", "config",
           "capture_warnings", "captureWarnings"]
