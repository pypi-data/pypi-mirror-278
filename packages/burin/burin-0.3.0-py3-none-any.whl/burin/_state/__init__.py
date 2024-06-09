"""
Burin State Options and Parameters

Copyright (c) 2022-2024 William Foster with BSD 3-Clause License
See included LICENSE file for details.
"""

# Python imports
import inspect
import os
import time


class _BurinConfig:
    """
    Stores configuration values for Burin.

    There should only be one instance of this within Burin and it contains the
    general configuration values that can be adjusted.
    """

    def __init__(self):
        """
        Sets the initial configuration values.
        """

        self.__logAsyncioTasks = True
        self.__logMultiprocessing = True
        self.__logProcesses = True
        self.__logThreads = True
        self.__raiseExceptions = True

    @property
    def logAsyncioTasks(self):
        """
        Whether asyncio task names should be available for inclusion in logs.

        Whatever value is set for this will be automatically converted using
        :func:`bool`.

        .. note::

            In Python 3.12 this was added to the standard :mod:`logging`
            module; it is supported here for all versions of Python compatible
            with Burin (including versions below 3.12).

            However; names were added to :class:`asyncio.Task` objects in
            Python 3.8, so in Python 3.7 the *taskName* attribute on a log
            record will always be **None**.
        """

        return self.__logAsyncioTasks

    @logAsyncioTasks.setter
    def logAsyncioTasks(self, value):
        self.__logAsyncioTasks = bool(value)

    @property
    def logMultiprocessing(self):
        """
        Whether multiprocessing info should be available for inclusion in logs.

        Whatever value is set for this will be automatically converted using
        :func:`bool`.
        """

        return self.__logMultiprocessing

    @logMultiprocessing.setter
    def logMultiprocessing(self, value):
        self.__logMultiprocessing = bool(value)

    @property
    def logProcesses(self):
        """
        Whether process info should be available for inclusion in logs.

        Whatever value is set for this will be automatically converted using
        :func:`bool`.
        """

        return self.__logProcesses

    @logProcesses.setter
    def logProcesses(self, value):
        self.__logProcesses = bool(value)

    @property
    def logThreads(self):
        """
        Whether threading info should be available for inclusion in logs.

        Whatever value is set for this will be automatically converted using
        :func:`bool`.
        """

        return self.__logThreads

    @logThreads.setter
    def logThreads(self, value):
        self.__logThreads = bool(value)

    @property
    def raiseExceptions(self):
        """
        Whether exceptions during handling should be propagated or ignored.

        Whatever value is set for this will be automatically converted using
        :func:`bool`.
        """

        return self.__raiseExceptions

    @raiseExceptions.setter
    def raiseExceptions(self, value):
        self.__raiseExceptions = bool(value)


config = _BurinConfig()

# Base for calculating the relative time of events
_internals = {
    "srcDir": None,
    "startTime": time.time()
}


# Setup local references to imports that aren't part of this package
__inspect = inspect
__osPath = os.path
def _set_src_dir(obj):
    """
    Sets the internal source directory of the library.

    This should be called only with an object in a module in the main Burin
    root directory.

    The :attr:`_internals` *srcDir* value can then be checked when walking
    through stack frames to determine when a frame is outside of Burin.

    :param obj: A class, function, attribute, or other object that
                :func:`inspect.getfile` can use to get the source path.
    :type obc: Any
    """

    _internals["srcDir"] = __osPath.dirname(__osPath.normcase(__inspect.getfile(obj)))


__all__ = ["config"]


# Clean up some things that aren't part of this package
del inspect
del os
del time
