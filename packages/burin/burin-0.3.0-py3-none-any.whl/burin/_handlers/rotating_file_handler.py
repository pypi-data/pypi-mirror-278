"""
Burin Rotating File Handler

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

# Burin imports
from .base_rotating_handler import BurinBaseRotatingHandler


class BurinRotatingFileHandler(BurinBaseRotatingHandler):
    """
    A handler that rotates the file when it reaches a certain size.

    This is derived from :class:`BurinBaseRotatingHandler`.

    The file is rotated once it reaches a specific size.  A limit can also be
    placed on how many rotated files are kept.
    """

    def __init__(self, filename, mode="a", maxBytes=0, backupCount=0,
                 encoding=None, delay=False, errors=None, level="NOTSET"):
        """
        This will initialize the handler to write to the file.

        The file will be rotated when it reaches *maxBytes* size.  The number
        of rotated files to keep is set by *backupCount*.

        When the files are rotated a number is appended to the filename in the
        order '.1', '.2', '.3', etc. until the *backupCount* is reached.  So a
        *backupCount* of 5 will result in 5 files other than the active log
        file being kept up to '*filename*.5'.  Once *backupCount* is reached
        the next time a rotate happens the oldest file will be removed.

        The active log file set with *filename* is always the file being
        written to.

        :param filename: The filename or path to write to.
        :type filename: str | pathlib.Path
        :param mode: The mode that the file is opened with.  This should be 'a'
                     in almost all use cases.  If 'w' is in the mode and
                     *maxBytes* != 0 then it will be replaced with 'a' as
                     otherwise the file will be truncated every time the
                     program runs which is counter-intuitive to a rotating log
                     file. (Default = 'a')
        :type mode: str
        :param maxBytes: The maximum size (in bytes) the file can be before a
                         rotation happens.  The rotation happens before an emit
                         so the file should never go above this size.  If this
                         is 0 then the file will never be rotated.  (Default =
                         0)
        :type maxBytes: int
        :param backupCount: How many rotated log files to keep.  If this is 0
                            then the file will not be rotated.  (Default = 0)
        :type backupCount: int
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

        # If rotation is desired then it doesn't make sense to use a "w" mode
        # as it would truncate logs from any previous runs
        if maxBytes > 0 and "w" in mode:
            mode = mode.replace("w", "a")

        if "b" not in mode:
            encoding = io.text_encoding(encoding)

        BurinBaseRotatingHandler.__init__(self, filename, mode, encoding=encoding,
                                          delay=delay, errors=errors, level=level)
        self.maxBytes = maxBytes
        self.backupCount = backupCount

    def do_rollover(self):
        """
        Does the rollover of the file.

        .. note::

            This uses :func:`os.replace` instead of the combination of
            :func:`os.remove` and :func:`os.rename` from the standard logging
            library.

            Functionally this should be the same, but it simplifies the
            operation slightly.
        """

        if self.stream is not None:
            self.stream.close()
            self.stream = None

        if self.backupCount > 0:
            for suffix in range(self.backupCount - 1, 0, -1):
                sourceFilename = self.rotation_filename(f"{self.baseFilename}.{suffix}")
                destFilename = self.rotation_filename(f"{self.baseFilename}.{suffix + 1}")

                if os.path.exists(sourceFilename):
                    os.replace(sourceFilename, destFilename)

            destFilename = self.rotation_filename(f"{self.baseFilename}.1")
            self.rotate(self.baseFilename, destFilename)

        if not self.delay:
            self.stream = self._open()

    def should_rollover(self, record):
        """
        Determines if a file rollover should occur.

        This uses the supplied record to check if the file would exceed the
        size limit that has been set.

        :param record: The log record being handled.
        :type record: BurinLogRecord
        :returns: Whether a file rotation should occur as the new record would
                  put the file past the size limit.
        :rtype: bool
        """

        # Ensure only regular files are rotated
        if os.path.exists(self.baseFilename) and not os.path.isfile(self.baseFilename):
            return False

        if self.stream is None:
            self.stream = self._open()

        if self.maxBytes > 0:
            msg = f"{self.format(record)}\n"
            self.stream.seek(0, os.SEEK_END)
            if (self.stream.tell() + len(msg)) > self.maxBytes:
                return True

        return False

    # Aliases for better compatibility to replace standard library logging
    doRollover = do_rollover
    shouldRollover = should_rollover
