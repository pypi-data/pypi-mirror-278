"""
Burin NT Event Log Handler

Copyright (c) 2022-2024 William Foster with BSD 3-Clause License
See included LICENSE file for details.

This module has some portions based on the Python standard logging library
which is under the following licenses:
Copyright (c) 2001-2024 Python Software Foundation; All Rights Reserved
Copyright (c) 2001-2022 Vinay Sajip. All Rights Reserved.
See included LICENSE file for details.
"""

# Python imports
import os.path

# Burin imports
from .._log_levels import CRITICAL, DEBUG, ERROR, INFO, WARNING
from .handler import BurinHandler


class BurinNTEventLogHandler(BurinHandler):
    """
    A handler which sends events to Windows NT Event Log.

    To use this handler you must be on a Windows system and have the `pywin32`
    package installed.
    """

    def __init__(self, appname, dllname=None, logtype="Application",
                 level="NOTSET"):
        """
        This sets the application name and allows using a specific dll.

        During initialization this will try to import the
        :mod:`win32evtlogutil` and :mod:`win32evtlog` modules from the
        `pywin32` package.  If this fails it will print a message to `stdout`
        and the handler that is created will not log anything.

        A registry entry for the *appname* will be created.  Also if *dllname*
        is **None** then *win32service.pyd* is used.  This can cause the
        resulting event logs to be quite large, so you can specify a different
        *dllname* with the message definitions you want to use.

        :param appname: The name of the application which will be added to the
                        registry.
        :type appname: str
        :param dllname: Specify a dll to use other than *win32service.pyd*.
        :type dllname: str
        :param logtype: The log type used to register the event logs.
        :type logtype: str
        :param level: The logging level of the handler.  (Default = 'NOTSET')
        :type level: int | str
        """

        BurinHandler.__init__(self, level=level)

        try:
            import win32evtlogutil
            import win32evtlog

            self.appname = appname
            self._welu = win32evtlogutil

            if not dllname:
                dllname = os.path.split(self._welu.__file__)
                dllname = os.path.split(dllname[0])
                dllname = os.path.split(dllname[0], r"win32service.pyd")

            self.dllname = dllname
            self.logtype = logtype

            # Admin privileges are required to add a source to the registry,
            # so handle the case where this may fail even for a regular user
            # adding to an existing source.
            try:
                self._welu.AddSourceToRegistry(appname, dllname, logtype)
            except Exception as exc:
                # Likely a pywintypes.error, but only raise the exception if
                # it's not a 0x5 "ERROR_ACCESS_DENIED" error
                if getattr(exc, "winerror", None) != 5:  # noqa: PLR2004
                    raise

            self.deftype = win32evtlog.EVENTLOG_ERROR_TYPE
            self.typemap = {
                DEBUG: win32evtlog.EVENTLOG_INFORMATION_TYPE,
                INFO: win32evtlog.EVENTLOG_INFORMATION_TYPE,
                WARNING: win32evtlog.EVENTLOG_WARNING_TYPE,
                ERROR: win32evtlog.EVENTLOG_ERROR_TYPE,
                CRITICAL: win32evtlog.EVENTLOG_ERROR_TYPE
            }
        except ImportError:
            print("The Python Win32 extensions for NT (service and event "
                  "logging) appear to be unavailable")
            self._welu = None

    def close(self):
        """
        Closes the handler.
        """

        BurinHandler.close(self)

    def emit(self, record):
        """
        Emits a log record.

        This will get the message ID, event category, and event type, then it
        will log the message to the NT event log.

        .. note::

            If the win32evtlogutil could not be imported during handler
            initialization then this will not do anything.

        :param record: The log record to emit.
        :type record: BurinLogRecord
        """

        if self._welu:
            try:
                msgId = self.get_message_id(record)
                category = self.get_event_category(record)
                evtType = self.get_event_type(record)
                msg = self.format(record)
                self._welu.ReportEvent(self.appname, msgId, category, evtType, [msg])
            except Exception:
                self.handle_error(record)

    def get_event_category(self, record): # noqa: ARG002
        """
        Returns the event category for the record.

        This can be overidden to specify a category, by default this just
        returns **0**.

        :param record: The log record being handled.  This is not used in this
                       basic method implementation.
        :type record: BurinLogRecord
        :returns: The event category for the record.
        :rtype: int
        """

        return 0

    def get_event_type(self, record):
        """
        Returns the event type for the record.

        A basic mapping of the standard log levels to Win32 event log types is
        used for this.  If you are using your own log levels or want to
        customise this process you can either override the *typemap* property
        of the handler, or override this method.

        :param record: The log record being handled.
        :type record: BurinLogRecord
        :returns: The Win32 event log type for the record.  If the log record's
                  level does not map to a type this will return the ERROR type.
        :rtype: int
        """

        return self.typemap.get(record.levelno, self.deftype)

    def get_message_id(self, record): # noqa: ARG002
        """
        Return the message ID for the record.

        This returns **1** be default which is the base message ID in
        *win32service.pyd*.  This can be changed or customised by overriding
        this method and crafting your log messages or records in a specific
        way to allow a lookup for each ID.

        :param record: The log record being handled.
        :type record: BurinLogRecord
        :returns: The event message ID for the log record.
        :rtype: int
        """

        return 1

    # Aliases for better compatibility to replace standard library logging
    getEventCategory = get_event_category
    getEventType = get_event_type
    getMessageId = get_message_id
