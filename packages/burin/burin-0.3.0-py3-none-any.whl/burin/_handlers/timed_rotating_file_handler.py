"""
Burin Timed Rotating File Handler

Copyright (c) 2022-2024 William Foster with BSD 3-Clause License
See included LICENSE file for details.

This module has some portions based on the Python standard logging library
which is under the following licenses:
Copyright (c) 2001-2024 Python Software Foundation; All Rights Reserved
Copyright (c) 2001-2022 Vinay Sajip. All Rights Reserved.
See included LICENSE file for details.
"""

# Python imports
from stat import ST_MTIME
import io
import os
import re
import time

# Burin imports
from .base_rotating_handler import BurinBaseRotatingHandler


# Values needed for calculations
_DAY_SECONDS = 24 * 60 * 60


class BurinTimedRotatingFileHandler(BurinBaseRotatingHandler):
    """
    A handler that rotates the file at specific intervals.

    This is derived from :class:`BurinBaseRotatingHandler`.

    The file is rotated once at the specified interval.  A limit can also be
    placed on how many rotated files are kept.
    """

    def __init__(self, filename, when="H", interval=1, backupCount=0,
                 encoding=None, delay=False, utc=False, atTime=None,
                 errors=None, level="NOTSET"):
        """
        This will initialize the handler to write to the file.

        The file will be rotated based on the *when*, *interval*, and
        *atTime* values.  The number of rotated files to keep is set by
        *backupCount*.

        +------------+------------------------+----------------------------+
        | *when*     | Interval type          | *atTime* usage             |
        +============+========================+============================+
        | 'S'        | Seconds                | Ignored                    |
        +------------+------------------------+----------------------------+
        | 'M'        | Minutes                | Ignored                    |
        +------------+------------------------+----------------------------+
        | 'H'        | Hours                  | Ignored                    |
        +------------+------------------------+----------------------------+
        | 'D'        | Days                   | Ignored                    |
        +------------+------------------------+----------------------------+
        | 'W0'-'W6'  | | Weeks                | Time of the day to rotate, |
        |            | | Weekday (0 = Monday) | default is midnight        |
        +------------+------------------------+----------------------------+
        | 'MIDNIGHT' | | Days                 | Time of the day to rotate, |
        |            | | Midnight or *atTime* | default is midnight        |
        +------------+------------------------+----------------------------+

        If using a weekday ``W0``-``W6`` value for *when* then the interval
        will be how many weeks between the rotation is desired.  Whereas if
        ``MIDNIGHT`` is used then the interval is how many days between
        rotation at either midnight or the specified time.

        .. note::

            In the standard :class:`logging.handlers.TimedRotatingFileHandler`
            intervals are supposed to be ignored if weekdays or midnight are
            set for *when*.  Although version 3.12.3 introduced this same
            functionality, this is likely inadvertent as the documentation
            still says it is ignored.

        When the files are rotated a time and/or date is appended to the
        filename until the *backupCount* is reached.  The :func:`time.strftime`
        format ``%Y-%m-%d_%H-%M-%S`` is used with later parts stripped off when
        not relevant for the rotation interval selected. Once *backupCount* is
        reached the next time a rotate happens the oldest file will be removed.

        The rotation interval is calculated (during initialization) based on
        the last modification time of the log file, or the current time if the
        file doesn't exist, to determine when the next rotation will occur.

        .. note::

            Rotation intervals for this class treat midnight as the beginning
            of the day, and not the end of it.  This differs from the standard
            :class:`logging.handlers.TimedRotatingFileHandler`.

            For example if the current time is a Tuesday (W1) and *when* is set
            to Wednesday (W2) without a specific *atTime*; then the next
            rotation will occur on the next logging event after 00:00 of
            Wednesday; not 00:00 of Thursday (as the standard library does)

        The active log file set with *filename* is always the file being
        written to.

        .. note::

            In Python 3.9 the *errors* parameter was adder to
            :class:`logging.handlers.TimedRotatingFileHandler`.  This is
            available here for all versions of Python compatible with Burin
            (including versions below 3.9).

        :param filename: The filename or path to write to.
        :type filename: str | pathlib.Path
        :param when: The type of interval to use when calculating the rotation.
                     Use the table above to see the available options and how
                     they impact the rotation interval.  (Default = 'H')
        :type when: str
        :param interval: The interval to use for the file rotation.  Use the
                         table above to see how this is used in determining the
                         rotation interval.  (Default = 1)
        :type interval: int
        :param backupCount: How many rotated log files to keep.  If this is 0
                            then the file will not be rotated.  (Default = 0)
        :type backupCount: int
        :param encoding: The text encoding to open the file with.
        :type encoding: str
        :param delay: Whether to delay opening the file until the first record
                      is emitted.  (Default = **False**)
        :type delay: bool
        :param utc: Whether to use UTC time or local time.  (Default =
                    **False**)
        :type utc: bool
        :param atTime: The time to use for weekday or 'midnight' (daily at set
                       time) rotations.  Use the table above to see how this is
                       used in determining the rotation interval.
        :type atTime: datetime.time
        :param errors: Specifies how encoding errors are handled.  See
                       :func:`open` for information on the appropriate values.
        :type errors: str
        :param level: The logging level of the handler.  (Default = 'NOTSET')
        :type level: int | str
        """

        encoding = io.text_encoding(encoding)
        weekdayLength = 2
        BurinBaseRotatingHandler.__init__(self, filename, "a", encoding=encoding,
                                          delay=delay, errors=errors, level=level)
        self.when = when.upper()
        self.backupCount = backupCount
        self.utc = utc
        self.atTime = atTime

        # Calculate the real rollover interval which is really just a number of
        # calculated seconds.
        if self.when == "S":
            self.interval = 1
            self.suffix = "%Y-%m-%d_%H-%M-%S"
            extMatchPattern = r"(?<!\d)\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}(?!\d)"
        elif self.when == "M":
            self.interval = 60  # one minute
            self.suffix = "%Y-%m-%d_%H-%M"
            extMatchPattern = r"(?<!\d)\d{4}-\d{2}-\d{2}_\d{2}-\d{2}(?!\d)"
        elif self.when == "H":
            self.interval = 60 * 60  # one hour
            self.suffix = "%Y-%m-%d_%H"
            extMatchPattern = r"(?<!\d)\d{4}-\d{2}-\d{2}_\d{2}(?!\d)"
        elif self.when in ("D", "MIDNIGHT"):
            self.interval = _DAY_SECONDS  # one day
            self.suffix = "%Y-%m-%d"
            extMatchPattern = r"(?<!\d)\d{4}-\d{2}-\d{2}(?!\d)"
        elif self.when.startswith("W"):
            self.interval = _DAY_SECONDS * 7  # one week
            if len(self.when) != weekdayLength:
                raise ValueError("You must specify a day for weekly rollover "
                                 f"from 0 to 6 (0 is Monday): {self.when}")
            if self.when[1] < "0" or self.when[1] > "6":
                raise ValueError("Invalid day specified for weekly rollover: "
                                 f"{self.when}")
            self.dayOfWeek = int(self.when[1])
            self.suffix = "%Y-%m-%d"
            extMatchPattern = r"(?<!\d)\d{4}-\d{2}-\d{2}(?!\d)"
        else:
            raise ValueError(f"Invalid rollover interval specified: {self.when}")

        # This is meant to match the datetime suffix in a filename.  The
        # pattern should ensure that this is not preceded or followed by digits
        # to reduce the number of false matches.
        self.extMatch = re.compile(extMatchPattern, re.ASCII)

        self.interval *= interval

        # In case a Path object was passed in ensure we have a string for the
        # filename
        filename = self.baseFilename

        mTime = os.stat(filename)[ST_MTIME] if os.path.exists(filename) else int(time.time())
        self.rolloverAt = self.compute_rollover(mTime)

    def compute_rollover(self, currentTime):
        """
        Determines the rollover time.

        This will used the specified time to determine the next rollover based
        on the interval set on the handler.

        :param currentTime: The current time to calculate the next rollover
                            from.
        :type currentTime: int
        :returns: The next rollover time.
        :rtype: int
        """

        # If rolling over at midnight or weekly then the current interval needs
        # to be calculated.  After that the interval is simple to determine.
        if self.when == "MIDNIGHT" or self.when.startswith("W"):
            baseTime = time.gmtime(currentTime) if self.utc else time.localtime(currentTime)
            currentHour = baseTime.tm_hour
            currentMinute = baseTime.tm_min
            currentSecond = baseTime.tm_sec
            currentWeekday = baseTime.tm_wday

            # Calculate seconds between now and next rotation
            if self.atTime is None:
                rotateTime = 0  # Midnight
            else:
                rotateTime = (((self.atTime.hour * 60) + self.atTime.minute) * 60) + self.atTime.second

            rotateDiff = rotateTime - ((((currentHour * 60) + currentMinute) * 60) + currentSecond)

            # If rotate time is before current time then rotation is tomorrow
            # so add a day.
            if rotateDiff <= 0:
                rotateDiff += _DAY_SECONDS
                currentWeekday = (currentWeekday + 1) % 7

            rolloverAt = currentTime + rotateDiff

            # If rolling over on a specific day of the week then adjustments
            # need to be made if that day if later this week, or next week.
            # Since the calculations above already get us to midnight (the next
            # day) then an extra day needs to be worked into these calculations
            # as well.
            if self.when.startswith("W"):
                if currentWeekday != self.dayOfWeek:
                    if currentWeekday < self.dayOfWeek:
                        daysToWait = self.dayOfWeek - currentWeekday
                    else:
                        daysToWait = 6 - currentWeekday + self.dayOfWeek + 1

                    rolloverAt += daysToWait * _DAY_SECONDS

                # Add the interval and adjust so this would fall into the
                # correct week.
                rolloverAt += self.interval - (_DAY_SECONDS * 7)
            else:
                # Add the interval if rolling over at midnight or a specific
                # time
                rolloverAt += self.interval - _DAY_SECONDS

            # Adjust in case DST changes between now and rollover
            if not self.utc:
                utcOffNow = baseTime.tm_gmtoff
                utcOffAtRollover = time.localtime(rolloverAt).tm_gmtoff
                utcOffDiff = utcOffNow - utcOffAtRollover
                if utcOffDiff != 0:
                    rolloverAt += utcOffDiff
        else:
            # Non-weekday or midnight calculations are much simpler
            rolloverAt = currentTime + self.interval

        return rolloverAt

    def do_rollover(self):
        """
        Does the rollover of the file.

        This will append  date-time to the filename of when the current
        interval started.  This will also remove extra files over the backup
        count.

        .. note::

            The date-time appended to filenames where *when* is set to a
            weekday (W0-W6) or midnight may not be accurate for the first file
            created.  This is because *atTime* - *interval* is unlikely to
            match the actual creation time for the first file.
        """

        currentTime = int(time.time())

        startTime = self.rolloverAt - self.interval
        if self.utc:
            startTuple = time.gmtime(startTime)
        else:
            startTuple = time.localtime(startTime)

            utcOffNow = time.localtime(currentTime).tm_gmtoff
            utcOffStart = startTuple.tm_gmtoff
            utcOffDiff = utcOffNow - utcOffStart
            if utcOffDiff != 0:
                startTuple = time.localtime(startTime + utcOffDiff)

        rotateFileName = self.rotation_filename(f"{self.baseFilename}.{time.strftime(self.suffix, startTuple)}")

        # Assume if the file exists the rollover has already happened
        if os.path.exists(rotateFileName):
            return

        if self.stream is not None:
            self.stream.close()
            self.stream = None

        self.rotate(self.baseFilename, rotateFileName)

        # Delete extra files if backup count is set
        if self.backupCount > 0:
            for filePath in self.get_files_to_delete():
                os.remove(filePath)

        # Reopen the file if not delaying
        if not self.delay:
            self.stream = self._open()

        # Calculate the next rollover
        self.rolloverAt = self.compute_rollover(currentTime)

    def get_files_to_delete(self):
        """
        Determines the files to delete when rolling over.

        :returns: A list of file paths to remove.
        :rtype: list[str]
        """

        dirName, baseName = os.path.split(self.baseFilename)
        fileNames = os.listdir(dirName)
        logFiles = []

        if self.namer is None:
            namePrefix = f"{baseName}."
            prefixLength = len(namePrefix)

            for fileName in fileNames:
                if fileName.startswith(namePrefix):
                    nameSuffix = fileName[prefixLength:]

                    if self.extMatch.fullmatch(nameSuffix):
                        logFiles.append(os.path.join(dirName, fileName))
        else:
            # Custom naming could mean almost file may be a log file, so check
            # for the datetime suffix in the filename and make sure this
            # handler could have created that file name.
            for fileName in fileNames:
                nameMatch = self.extMatch.search(fileName)

                while nameMatch:
                    namerName = self.namer(f"{self.baseFilename}.{nameMatch[0]}")

                    if os.path.basename(namerName) == fileName:
                        logFiles.append(os.path.join(dirName, fileName))
                        break

                    nameMatch = self.extMatch.search(fileName, nameMatch.start() + 1)

        if len(logFiles) < self.backupCount:
            logFiles = []
        else:
            logFiles.sort()
            logFiles = logFiles[:len(logFiles) - self.backupCount]

        return logFiles

    def should_rollover(self, record):  # noqa: ARG002
        """
        Determines if a rollover should occur.

        .. note::

            The *record* parameter is not used, it is included to keep the
            method signatures the same for all subclasses of
            :class:`BurinBaseRotatingHandler`

        .. note::

            In Python 3.11
            :meth:`logging.handlers.TimedRotatingFileHandler.shouldRollover`
            was changed to ensure that if the target is not currently a regular
            file the check is skipped and the next one is scheduled.
            Previously checks simply ran and failed repeatedly.  This change is
            incorporated here for all versions of Python compatible with Burin
            (including versions below 3.11).

        :param record: The log record.  (Not used)
        :type record: BurinLogRecord
        :returns: Whether a rollover is scheduled to occur.
        :rtype: bool
        """

        currentTime = int(time.time())
        if currentTime >= self.rolloverAt:
            # Ensure only regular files are ever rolled over
            if os.path.exists(self.baseFilename) and not os.path.isfile(self.baseFilename):
                # Avoid repeated checks if existing file isn't a regular
                # right now
                self.rolloverAt = self.compute_rollover(currentTime)
                return False

            return True

        return False

    # Aliases for better compatibility to replace standard library logging
    computeRollover = compute_rollover
    doRollover = do_rollover
    getFilesToDelete = get_files_to_delete
    shouldRollover = should_rollover
