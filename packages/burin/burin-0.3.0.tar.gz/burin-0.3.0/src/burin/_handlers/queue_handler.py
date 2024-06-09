"""
Burin Queue Handler

Copyright (c) 2022-2024 William Foster with BSD 3-Clause License
See included LICENSE file for details.

This module has some portions based on the Python standard logging library
which is under the following licenses:
Copyright (c) 2001-2024 Python Software Foundation; All Rights Reserved
Copyright (c) 2001-2022 Vinay Sajip. All Rights Reserved.
See included LICENSE file for details.
"""

# Python imports
import copy

# Burin imports
from .handler import BurinHandler


class BurinQueueHandler(BurinHandler):
    """
    A handler that supports logging messages to a queue.

    This can be used along with :class:`BurinQueueListener` to allow one
    process or thread in a program handle logging output which may consist of
    slow operations like file writing or sending emails.  This can be useful in
    Web or service applications where responsiveness is important in worker
    processes and threads.

    Logs records are added to the queue by each :class:`BurinQueueHandler` and
    then processed and output by the :class:`BurinQueueListener`.
    """

    def __init__(self, queue, level="NOTSET"):
        """
        This will initialize the handler and set the queue to use.

        :param queue: This must be any queue like object; it does not need to
                      support the task tracking API.
        :type queue: queue.Queue | queue.SimpleQueue | multiprocessing.Queue
        :param level: The logging level of the handler.  (Default = 'NOTSET')
        :type level: int | str
        """

        BurinHandler.__init__(self, level=level)
        self.queue = queue

    def emit(self, record):
        """
        Emits a log record.

        This will prepare the record and then add it to the queue.

        :param record: The log record to emit.
        :type record: BurinLogRecord
        """

        try:
            self.enqueue(self.prepare(record))
        except Exception:
            self.handle_error(record)

    def enqueue(self, record):
        """
        Enqueues a log record.

        This uses *put_nowait* on the queue to add the record.  If blocking,
        timeoutes, or custom queueing is required this should be overridden.

        :param record: The log record being handled.
        :type record: BurinLogRecord
        """

        self.queue.put_nowait(record)

    def prepare(self, record):
        """
        Prepares a log record for queueing.

        This will format the record and remove any unpickleable elements from
        it.  Both the *message* and *msg* properties of the record will be set
        to the same value and *args*, *kwargs*, *exc_info*, *exc_text*, and
        *stack_info* will all be set to **None**.

        .. note::

            This makes a copy of the record instead of altering the original
            one.  This way other handlers in the chain will still be able to
            process the original record.

        This can be overidden to change how the record is prepared.  For
        example to convert the record into some other format, or to create a
        copy of the record for enqueueing while keeping the original.

        :param record: The log record to prepare for enqueueing.
        :type record: BurinLogRecord
        :returns: The record prepared for enqueueing.
        :rtype: BurinLogRecord
        """

        record = copy.copy(record)

        msg = self.format(record)
        record.message = msg
        record.msg = msg
        record.args = None
        record.kwargs = None
        record.exc_info = None
        record.exc_text = None
        record.stack_info = None

        return record
