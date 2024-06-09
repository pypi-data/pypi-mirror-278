"""
Burin Base Rotating Handler

Copyright (c) 2022-2024 William Foster with BSD 3-Clause License
See included LICENSE file for details.
"""

# Python imports
import os

# Burin imports
from .file_handler import BurinFileHandler


class BurinBaseRotatingHandler(BurinFileHandler):
    """
    Base class for handlers that rotate log files.

    This is derived from :class:`BurinFileHandler`.

    This should not be instantiated directly except within a subclass
    *__init__* method.
    """

    namer = None
    rotator = None

    def __init__(self, filename, mode, encoding=None, delay=False, errors=None,
                 level="NOTSET"):
        """
        This will initialize the handler for outputting to a file.

        :param filename: The filename or path to write to.
        :type filename: str | pathlib.Path
        :param mode: The mode that the file is opened with.
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

        BurinFileHandler.__init__(self, filename, mode=mode, encoding=encoding,
                                  delay=delay, errors=errors, level=level)
        self.mode = mode
        self.encoding = encoding
        self.errors = errors

    def do_rollover(self):
        """
        This method should perform the rotation of the file.

        This should be implemented within a subclass and will only raise a
        :exc:`NotImplementedError` in this base class.

        :raises NotImplementedError: As this is not implemented in the base
                                     class.
        """

        raise NotImplementedError("do_rollover must be implemented by"
                                  "BurinBaseRotatingHandler subclasses")

    def emit(self, record):
        """
        Emits the record to the file.

        This will check if the file should be rotated by calling
        *should_rollover* and if that returns **True** it calls *do_rollover*
        to perform the actual rotation.

        :param record: The log record to emit.
        :type record: BurinLogRecord
        """

        try:
            if self.should_rollover(record):
                self.do_rollover()

            BurinFileHandler.emit(self, record)
        except Exception:
            self.handle_error(record)

    def rotate(self, source, dest):
        """
        Rotate the current log.

        This will call the *rotator* attribute of the handler, if it is
        callable, along with the source and destination.  If the attribute
        isn't callable (it defaults to **None**), then the source is simply
        renamed to the destination.

        .. note::

            Default rotation is done using :func:`os.replace` instead of
            :func:`os.rename` which is used in the standard
            :class:`logging.BaseRotatingHandler`.  This is so the renaming
            operation is more consistent across different platforms.

        :param source: The source filename to rotate.
        :type source: string | Path
        :param dest: The destination filename.
        :type dest: string | Path
        """

        if callable(self.rotator):
            self.rotator(source, dest)
        elif os.path.exists(source):
            os.replace(source, dest)

    def rotation_filename(self, defaultName):
        """
        Modifies the filename when rotating.

        This is provided so that a method for customising filenames can be
        used during rotation.

        If the *namer* attribute of the handler is callable then it is passed
        the *defaultName* and the resulting value is returned.  If it is not
        callable then the *defaultName* value is returned unchanged.

        :param defaultName: The default name for the file.
        :type defaultName: str
        :returns: The name to be used for the file rotation.
        :rtype: str
        """

        return self.namer(defaultName) if callable(self.namer) else defaultName

    def should_rollover(self, record):
        """
        This method should check if the rotation of the file should be done.

        This should be implemented within a subclass and will only raise a
        :exc:`NotImplementedError` in this base class.

        .. note::

            The *record* parameter is needed for the
            :class:`BurinRotatingFileHandler`, so to ensure the signature is
            the same all subclasses should include it whether they use it or
            not.

        :param record: The log record.  (Not used for all subclasses)
        :type record: BurinLogRecord
        :raises NotImplementedError: As this is not implemented in the base
                                     class.
        """

        raise NotImplementedError("should_rollover must be implemented by"
                                  "BurinBaseRotatingHandler subclasses")

    # Aliases for better compatibility to replace standard library logging
    # rotation_filename is not aliased as it never existed in the standard
    # library with the old camel casing
    doRollover = do_rollover
    shouldRollover = should_rollover
