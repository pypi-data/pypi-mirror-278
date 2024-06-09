.. currentmodule:: burin

========
Handlers
========

Handlers are responsible for emitting the log record to a specific destination.
All handlers within Burin are derived from the :class:`BurinHandler` class.

One feature of all Burin handlers is the ability to set the handler's log level
when it is created.  Every handler class has an optional ``level`` parameter for
this so :meth:`BurinHandler.set_level` doesn't need to be called seperately.
The default level for every handler is :data:`NOTSET`.

.. note::

    The handlers in the Burin library are not usable with the standard
    :mod:`logging` package, and vice-versa.  Using :mod:`logging` handlers with
    Burin or Burin handlers with :mod:`logging` will cause issues and may
    result in exceptions or lost logs.

Below is a list of all handlers available within Burin.  After that detailed
descriptions of each handler is provided.

.. autosummary::
    :nosignatures:

    BurinBaseRotatingHandler
    BurinBufferingHandler
    BurinDatagramHandler
    BurinFileHandler
    BurinHandler
    BurinHTTPHandler
    BurinMemoryHandler
    BurinNTEventLogHandler
    BurinNullHandler
    BurinQueueHandler
    BurinQueueListener
    BurinRotatingFileHandler
    BurinSMTPHandler
    BurinSocketHandler
    BurinStreamHandler
    BurinSyslogHandler
    BurinTimedRotatingFileHandler
    BurinWatchedFileHandler

------------------------
BurinBaseRotatingHandler
------------------------

This is the base rotating handler which can be used by any handlers that need
to rotate files.  This should not be used directly but instead can be inherited
from to create custom handlers.

.. autoclass:: BurinBaseRotatingHandler
    :members: do_rollover, emit, rotate, rotation_filename, should_rollover

---------------------
BurinBufferingHandler
---------------------

This is a base buffering handler which can be used to create other handlers
which require a buffering pattern.  This should not be used directly but
instead can be inherited from to create custom handlers.

.. autoclass:: BurinBufferingHandler
    :members: close, emit, flush, should_flush

--------------------
BurinDatagramHandler
--------------------

This handler can be used to send logs through a datagram socket to another
Python application.

.. autoclass:: BurinDatagramHandler
    :members: make_socket, send

----------------
BurinFileHandler
----------------

This handler allows for simply writing logs out to a file.

.. autoclass:: BurinFileHandler
    :members: close, emit

------------
BurinHandler
------------

This is the base handler class that all other handlers in Burin are derived
from.  This should not be used directly but instead can be inherited from to
create custom handlers.

.. autoclass:: BurinHandler
    :members: acquire, close, create_lock, flush, format, handle, handle_error,
              release, set_formatter, set_level

    .. autoproperty:: name

----------------
BurinHTTPHandler
----------------

This handler can send logs to another service using HTTP.

.. autoclass:: BurinHTTPHandler
    :members: emit, get_connection, map_log_record

------------------
BurinMemoryHandler
------------------

This handler can buffer logs in memory until a specified capacity is reached.

.. autoclass:: BurinMemoryHandler
    :members: close, flush, set_target, should_flush

----------------------
BurinNTEventLogHandler
----------------------

This handler can log to the Windows event log; this requires the `pywin32`
package.

.. autoclass:: BurinNTEventLogHandler
    :members: close, emit, get_event_category, get_event_type, get_message_id

----------------
BurinNullHandler
----------------

This handler doesn't do anything, but can be used to ensure a logger has a
configured handler that doesn't actually output to anything (not even
`sys.stderr`).  This may be useful in libraries where you want to use Burin
if it's available, but want to let the application configure the output
handlers.

.. autoclass:: BurinNullHandler
    :class-doc-from: class
    :members: create_lock, emit, handle

-----------------
BurinQueueHandler
-----------------

This handler adds all logs to a queue which a :class:`BurinQueueListener` can
then process.  This can be useful in a multiprocess application to have one
process handle all of the actual logging (and I/O involved) while the others
just add to the queue.

.. autoclass:: BurinQueueHandler
    :members: emit, enqueue, prepare

------------------
BurinQueueListener
------------------

This can be paired with :class:`BurinQueueHandler` to have one process for a
queue of logs which multiple handlers add to.

.. autoclass:: BurinQueueListener
    :class-doc-from: class

------------------------
BurinRotatingFileHandler
------------------------

This handler can automatically rotate a log file when it reaches a specific
size.

.. autoclass:: BurinRotatingFileHandler
    :members: do_rollover, should_rollover

----------------
BurinSMTPHandler
----------------

This handler can send logs through email using a SMTP server.

.. autoclass:: BurinSMTPHandler
    :members: emit, get_subject

------------------
BurinSocketHandler
------------------

This handler can send pickled log records through a socket to another Python
application.

.. autoclass:: BurinSocketHandler
    :members: close, create_socket, emit, handle_error, make_pickle,
              make_socket, send

------------------
BurinStreamHandler
------------------

This handler can write logs to an I/O stream.

.. autoclass:: BurinStreamHandler
    :members: emit, flush, set_stream

------------------
BurinSyslogHandler
------------------

This handler can write logs out using Syslog.

.. autoclass:: BurinSyslogHandler
    :members: close, create_socket, emit, encode_priority

-----------------------------
BurinTimedRotatingFileHandler
-----------------------------

This handler can rotate log files based on a timing pattern.

.. autoclass:: BurinTimedRotatingFileHandler
    :members: compute_rollover, do_rollover, get_files_to_delete,
              should_rollover

-----------------------
BurinWatchedFileHandler
-----------------------

This handler watches the file it is writing to and will close and reopen it
automatically if it detects any changes.

.. autoclass:: BurinWatchedFileHandler
    :members: emit, reopen_if_needed
