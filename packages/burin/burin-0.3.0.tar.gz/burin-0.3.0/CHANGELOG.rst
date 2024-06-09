--------------------
0.3.0 - June 8, 2024
--------------------

^^^^^^^^^^^^^^^^^^^^^^
Features and Additions
^^^^^^^^^^^^^^^^^^^^^^

 * Added option for ``BurinSMTPHandler`` to use ``ssl.SSLContext`` for
   *secure* parameter.
 * Added support for ``BurinSMTPHandler`` to connect using STARTTLS if *secure*
   is set and no credentials are.
 * Added support for intervals to be used with
   ``BurinTimedRotatingFileHandler`` if *when* is a weekday (*W0*-*W6*) or
   *MIDNIGHT*.
 * Changed ``BurinTimedRotatingFileHandler`` to treat midnight as the beginning
   of the day if *when* is a weekday (*W0*-*W6*) or *MIDNIGHT*.
 * Added kerword args of log record to ``BurinHandler.handle_error`` output.

^^^^^^^^
Internal
^^^^^^^^

 * Modified all handlers to no longer import from any handler in the standard
   ``logging`` library.
 * Changed ``_BurinDollarStyle`` to call ``_BurinPercentStyle.__init__``
   directly instead of *super()*.
 * Refactored several tests and added tests for ``BurinHandler`` and
   ``BurinStreamHandler``.

^^^^^^^^^^^^
Dependencies
^^^^^^^^^^^^

 * Updated Ruff to 0.4.8
 * Updated PyTest to 8.2.2
 * Updated Coverage to 7.5.3
 * Updated Sphinx to 7.3.7

^^^^^^^^^^^^^^^^^^^^^
Build and Environment
^^^^^^^^^^^^^^^^^^^^^

 * Moved local project to Hatch 1.12.0 and updated Github Action to also use
   this version.

-------------------------
0.2.0 - February 10, 2024
-------------------------

^^^^^^^^^^^^^^^^^^^^^^^^^
Removals and Deprecations
^^^^^^^^^^^^^^^^^^^^^^^^^

 * Python 3.6 support removed
 * Python 3.7 support is deprecated and will be removed in a future release

^^^^^^^^^^^^^^^^^^^^^^
Features and Additions
^^^^^^^^^^^^^^^^^^^^^^

 * Added support and feature compatiblity for Python 3.12

   * Added ``burin.config.logAsyncioTasks`` option and *taskName* property to
     ``BurinLogRecord`` (*taskName* is always **None** on Python 3.7 as task
     names weren't added to asyncio until 3.8)
   * Added ``burin.get_handler_by_name`` function
   * Added ``burin.get_handler_names`` functions
   * Added ``BurinLogger.get_children`` method
   * Added ``BurinFilter`` and ``BurinFilterer`` classes so that filterer
     checks can return a ``BurinLogRecord`` instance
   * Added checking of *flushOnClose* for handlers during shutdown

 * Added support and feature compatiblity for Python 3.11

   * Added ``burin.get_level_names_mapping`` function
   * Added ``BurinSyslogHandler.create_socket`` method
   * Improved ``BurinTimedRotatingFileHandler.should_rollover`` so if target is
     not a normal file the check doesn't run repeatedly and will get
     rescheduled
   * Improved efficiency of finding first non-internal frame during logging
     event, especially if current frame is unavailable
   * Added access denied exception handling on initialization of
     ``BurinNTEventLogHandler``

 * Added optional *level* parameter to all burin handlers so a separate
   ``BurinHandler.set_level`` call isn't needed after creating a handler
 * Enabled a single dictionary argument to be used with '{' and '$' style log
   records, just as they could be used for '%' style records
 * Added *filedelay* parameter to ``burin.basic_config``
 * If running on Python 3.11 or greater then '$' style formatters will use
   ``string.Template.is_valid()`` for more efficient validation checking
 * Added ``BurinPercentLogRecord`` to process records with '%' style
   formatting
 * ``BurinLogRecord`` is now a base class that doesn't do any formatting itself

^^^^^
Fixes
^^^^^

 * Fixed potential referencing issues by moving attributes
   ``logMultiprocessing``, ``logProcesses``, ``logThreads``, and
   ``raiseExceptions`` to new ``burin.config`` object
 * Fixed issue where '$' style formatters would return **None** after formatting
 * Fixed extra arguments not getting passed through from ``burin.exception``
   and ``BurinLogger.exception``
 * Fixed ``NOTSET`` log level missing from main burin module
 * Fixed ``burin.get_level_name`` return value for unknown level names
 * Fixed ``BurinBufferingFormatter`` not assigning default formatter properly
 * Fixed issue where ``BurinLogRecord.msecs`` could round to 1000 (based on
   Python 3.11 fix)
 * Fixed $ style formatter to use correct time search pattern (based on Python
   3.11 fix)

^^^^^^^^
Internal
^^^^^^^^

 * Created internal package _log_records
 * Renamed internal package _logging to _loggers
 * ``BurinHandler`` no longer inherits from ``logging.Handler``, aside from
   Burin specific changes though functionality should remain identical
 * In fallback ``current_frame`` function the exception object itself is used
   instead of going through ``sys``
 * More methods or other functions from the standard ``logging`` library have
   been re-created or overridden in Burin classes

^^^^^^^^^^^^
Dependencies
^^^^^^^^^^^^

 * Replaced Flake8 with Ruff as dev dependency for linting
 * Updated Sphinx doc dependency to 7.2.6
 * Updated sphinx-rtd-theme doc dependency to 2.0.0
 * Added Pytest and Coverage dependencies for testing
 * Removed Flit dependency for building

^^^^^^^^^^^^^^^^^^^^^
Build and Environment
^^^^^^^^^^^^^^^^^^^^^

 * Pipenv is no longer used in the project, so all related files (Pipfile,
   Pipfile.lock) have been removed
 * Hatch is now used for both environment management, task running, and
   building

--------------------
0.1.0 - June 2, 2022
--------------------

 * First formal release.
