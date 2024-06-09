"""
Burin Watched File Handler

Copyright (c) 2022-2024 William Foster with BSD 3-Clause License
See included LICENSE file for details.

This module has some portions based on the Python standard logging library
which is under the following licenses:
Copyright (c) 2001-2024 Python Software Foundation; All Rights Reserved
Copyright (c) 2001-2022 Vinay Sajip. All Rights Reserved.
See included LICENSE file for details.
"""

# Python imports
import io
import os
from stat import ST_DEV, ST_INO

# Burin imports
from .file_handler import BurinFileHandler


class BurinWatchedFileHandler(BurinFileHandler):
    """
    A handler that watches for changes to the file.

    If the file this is logging to changes it will close and then reopen the
    file.

    This is intended for use on Unix/Linux systems and checks for device or
    inode changes.  Such changes would occur if a program like *logrotate* was
    to rotate the file.

    This should not be used on Windows and is not needed as log files are
    opened with exclusive locks and cannot be moved or renamed when in use.
    """

    def __init__(self, filename, mode="a", encoding=None, delay=False,
                 errors=None, level="NOTSET"):
        """
        This will setup the handler and stat the file.

        :param filename: The filename or path to write to.
        :type filename: str | pathlib.Path
        :param mode: The mode that the file is opened with.  (Default = 'a')
        :type mode: str
        :param encoding: The text encoding to open the file with.
        :type encoding: str
        :param delay: Whether to delay opening the file until the first record
                      is emitted.  (Default = **False**)
        :type delay: bool
        :param errors: Specifies how encoding errors are handled.  See
                       :func:`open` for information on the appropriate values.
        :type errors: str
        :param level: The logging level of the handler.  (Default = 'NOTSET')
        :type level: int | str
        """

        if "b" not in mode:
            encoding = io.text_encoding(encoding)

        BurinFileHandler.__init__(self, filename, mode=mode, encoding=encoding,
                                  delay=delay, errors=errors, level=level)

        self.dev = -1
        self.ino = -1
        self._statstream()

    def emit(self, record):
        """
        Emits the record to the file.

        This will check if the file needs to be reopened before writing to it.

        :param record: The log record to emit.
        :type record: BurinLogRecord
        """

        self.reopen_if_needed()
        BurinFileHandler.emit(self, record)

    def reopen_if_needed(self):
        """
        Reopens the log file if needed.

        This checks if the underlying file has changed and if it has it closes
        and then reopens the file to get the current stream.
        """

        try:
            statResult = os.stat(self.baseFilename)
        except FileNotFoundError:
            statResult = None

        if (self.stream is not None and
            (statResult is None or statResult[ST_DEV] != self.dev or statResult[ST_INO] != self.ino)):
            # Clean up existing file handle
            self.stream.flush()
            self.stream.close()

            # Clear the set stream in cause _open fails
            self.stream = None

            # Open and stat the new stream
            self.stream = self._open()
            self._statstream()

    # Aliases for better compatibility to replace standard library logging
    reopenIfNeeded = reopen_if_needed

    def _statstream(self):
        if self.stream is not None:
            statResult = os.fstat(self.stream.fileno())
            self.dev = statResult[ST_DEV]
            self.ino = statResult[ST_INO]
