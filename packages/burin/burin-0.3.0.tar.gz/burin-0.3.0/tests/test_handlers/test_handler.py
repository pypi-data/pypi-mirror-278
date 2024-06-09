"""
Burin Handler Tests

Copyright (c) 2024 William Foster with BSD 3-Clause License
See included LICENSE file for details.
"""

# Python imports
from io import StringIO
import os
import signal
from threading import Event, Thread
import time

# PyTest imports
import pytest

# Burin import
import burin

# Tests imports
from ..helpers import (coverage_safe_exit, requires_fork_with_threading,
                       requires_register_at_fork, requires_threading)


class TestHandler:
    """
    Tests the base handler class.
    """

    def test_reference(self, basic_handler):
        """
        Tests that internal reference is created properly when instantiated.
        """

        refHandler = basic_handler()
        assert burin._handlers._handlerList[-1]() is refHandler

    def test_name(self, basic_handler):
        """
        Tests setting a name for a handler and the references it creates.
        """

        nameHandler = basic_handler()
        assert nameHandler.name is None

        # Set a name and check the reference
        testName1 = "Test_Handler_Name_1"
        nameHandler.name = testName1
        assert burin._handlers._handlers[testName1] is nameHandler

        # Change the name and check again
        testName2 = "Test_Handler_Name_2"
        nameHandler.name = testName2
        assert testName1 not in burin._handlers._handlers
        assert burin._handlers._handlers[testName2] is nameHandler

        # Change to None and check the reference is gone
        nameHandler.name = None
        assert nameHandler not in burin._handlers._handlers.valuerefs()

    def test_close_no_name(self, basic_handler):
        """
        Tests closing a handler that hasn't had a name set.
        """

        closeHandler = basic_handler()
        closeHandler.close()
        assert closeHandler._closed

    def test_close_with_name(self, basic_handler):
        """
        Tests closing a handler that has had a name set.
        """

        nameCloseHandler = basic_handler()
        testName = "Test_Handler_Close"
        nameCloseHandler.name = testName
        assert burin._handlers._handlers[testName] is nameCloseHandler

        nameCloseHandler.close()
        assert nameCloseHandler._closed
        assert testName not in burin._handlers._handlers

    def test_set_level(self, basic_handler):
        """
        Tests setting the level through instantiation and method.
        """

        # Test through instantiation
        levelHandler = basic_handler(burin.WARNING)
        assert levelHandler.level == burin.WARNING

        # Test through method
        levelHandler.set_level(burin.INFO)
        assert levelHandler.level == burin.INFO

        # Ensure invalid levels aren't set
        invalidLevelName = "UNKNOWN"
        with pytest.raises(ValueError, match=f"Unknown level: '{invalidLevelName.upper()}'"):
            levelHandler.set_level(invalidLevelName)

        assert levelHandler.level == burin.INFO

    def test_formatter_default(self, basic_handler, basic_record):
        """
        Tests that not setting the formatter works properly using the default.
        """

        formatRecord = basic_record()
        assert basic_handler().format(formatRecord) == burin._formatters._defaultFormatter.format(formatRecord)

    def test_formatter_set(self, basic_handler, basic_record):
        """
        Tests setting a formatter on a handler.
        """

        testFormat = "{name}: {message}"
        testFormatter = burin.BurinFormatter(testFormat, style="{")
        formatHandler = basic_handler()
        formatHandler.set_formatter(testFormatter)
        formatRecord = basic_record()

        assert formatHandler.formatter is testFormatter
        assert formatHandler.format(formatRecord) == testFormatter.format(formatRecord)

    def test_emit(self, basic_handler, basic_record):
        """
        Tests the basic handler emit is not implemented.
        """

        with pytest.raises(NotImplementedError):
            basic_handler().emit(basic_record())

    def test_handler_no_filter(self, basic_handler, basic_record):
        """
        Tests the basic handler handle call.
        """

        # Since emit is not implemented on the base handler this will raise
        # an exception
        with pytest.raises(NotImplementedError):
            basic_handler().handle(basic_record())

    def test_handler_filter(self, basic_handler, basic_record):
        """
        Tests that filtering occurs properly on the handler.
        """

        passFilter = burin.BurinFilter()
        filterHandler = basic_handler()
        filterHandler.add_filter(passFilter)
        filterRecord = basic_record()

        # Emit should get called and raise the error on the base handler if
        # the filtering passes
        with pytest.raises(NotImplementedError):
            filterHandler.handle(filterRecord)

        rejectFilter = burin.BurinFilter("REJECTED")
        filterHandler.add_filter(rejectFilter)

        assert filterHandler.handle(filterRecord) is False

    def test_handle_error_no_raise(self, basic_handler, basic_record, capsys):
        """
        Tests handler error processing with raising exceptions disabled.
        """

        burin.config.raiseExceptions = False

        errorHandler = basic_handler()
        errorRecord = basic_record()

        # Raise an actual exception as it is used when handling the error
        try:
            raise Exception("handle_error test")
        except Exception:
            errorHandler.handle_error(errorRecord)

        handleErrorOutput = capsys.readouterr().err
        assert len(handleErrorOutput) == 0

    def test_handle_error(self, basic_handler, basic_record, capsys):
        """
        Tests handler error processing.
        """

        burin.config.raiseExceptions = True

        errorHandler = basic_handler()
        errorRecord = basic_record()

        # Raise an actual exception as it is used when handling the error
        try:
            raise Exception("handle_error test")
        except Exception:
            errorHandler.handle_error(errorRecord)

        handleErrorOutput = capsys.readouterr().err
        assert handleErrorOutput.startswith("--- Burin Logging error ---")

    @requires_threading
    def test_handler_lock_explicit(self, basic_handler):
        """
        Tests that the handler lock works properly when used explicitly.
        """

        lockHandler = basic_handler()

        sleepTime = 0.015
        timeoutTime = 0.1
        acquireTimes = {
            "main-acquire": None,
            "main-reacquire": None,
            "main-reentry": None,
            "thread-acquire": None,
        }

        def _acquire_handler_lock():
            """
            Acquires the lock handler, sleeps, then releases the lock.
            """

            lockHandler.acquire()
            acquireTimes["thread-acquire"] = time.time()
            time.sleep(sleepTime)
            lockHandler.release()

        acquireThread = Thread(target=_acquire_handler_lock)

        # Acquire the lock then start the thread
        lockHandler.acquire()
        acquireTimes["main-acquire"] = time.time()
        acquireThread.start()

        # Sleep then try lock re-entry
        time.sleep(sleepTime)
        lockHandler.acquire()
        acquireTimes["main-reentry"] = time.time()

        # Sleep, release (twice), sleep, then try to re-acquire
        time.sleep(sleepTime)
        lockHandler.release()
        lockHandler.release()
        time.sleep(sleepTime)
        lockHandler.acquire()
        acquireTimes["main-reacquire"] = time.time()
        lockHandler.release()

        # Join the thread and compare times
        acquireThread.join(timeoutTime)
        assert acquireThread.is_alive() is False
        assert acquireTimes["main-acquire"] < acquireTimes["main-reentry"]
        assert acquireTimes["main-reentry"] < acquireTimes["thread-acquire"]
        assert acquireTimes["thread-acquire"] < acquireTimes["main-reacquire"]

    @requires_fork_with_threading
    @requires_register_at_fork
    def test_handler_lock_after_fork_reinit(self, basic_record, monkeypatch):
        """
        Tests that handler locks are re-initialized properly after a fork.
        """

        logStream = StringIO()

        class _ForkHandler(burin.BurinHandler):
            def emit(self, record):
                msg = self.format(record)
                logStream.write(msg + "\n")
                logStream.flush()

        testHandler = _ForkHandler()
        assert len(burin._threading._fork_protection._at_fork_reinit_lock_weakset) > 0

        locks_held__ready_to_fork = Event()
        fork_complete__release_locks_and_end = Event()

        def _lock_holder():
            """
            Acquires the burin and handler locks, then releases on signal
            """

            with burin._threading._BurinLock, testHandler.lock:
                # Signal that the main thread can fork
                locks_held__ready_to_fork.set()

                # Wait for the signal that the fork completed before running
                # out the rest of the thread
                fork_complete__release_locks_and_end.wait(0.5)

        lockHolderThread = Thread(target=_lock_holder)
        lockHolderThread.start()

        locks_held__ready_to_fork.wait()
        pid = os.fork()
        if pid == 0:
            # Child
            try:
                childRecord = basic_record(msg="Child is not deadlocked")
                testHandler.handle(childRecord)
            finally:
                with monkeypatch.context() as monkey:
                    monkey.setattr(os, "_exit", coverage_safe_exit)
                    os._exit(0)
        else:
            # Parent
            parentRecord = basic_record(msg="Parent is not deadlocked")
            testHandler.handle(parentRecord)
            lockHolderThread.join()

            maxWait = 0.5
            waitInterval = 0.05
            waitTotal = 0
            childPid, childStatus = os.waitpid(pid, os.WNOHANG)

            # Coverage is ignored for these as they are to try and clean up in
            # the case that the test failed to run properly
            while childPid != 0: # pragma: no cover
                if waitTotal >= maxWait:
                    break

                time.sleep(waitInterval)
                waitTotal += waitInterval

            if childPid != 0: # pragma: no cover
                try:
                    os.kill(pid, signal.SIGKILL)
                    os.waitpid(pid, 0)
                except OSError:
                    pass

                pytest.fail(reason="child process appears to be deadlocked "
                            "after fork", pytrace=False, msg="parent process "
                            "did not detect child exit within timeout limit")

            if hasattr(os, "waitstatus_to_exitcode"):
                # Only in Python 3.9+
                childExitCode = os.waitstatus_to_exitcode(childStatus)
            else:
                childExitCode = os.WEXITSTATUS(childStatus) if os.WIFEXITED(childStatus) else -1

            assert childExitCode == 0

    def test_repr(self, basic_handler):
        """
        Tests that the handler class representation string is correct.
        """

        # Check based on default level
        reprHandler = basic_handler()
        assert repr(reprHandler) == "<BurinHandler (NOTSET)>"

        # Confirm altering the level also changes the representation
        reprHandler.set_level(burin.WARNING)
        assert repr(reprHandler) == "<BurinHandler (WARNING)>"
