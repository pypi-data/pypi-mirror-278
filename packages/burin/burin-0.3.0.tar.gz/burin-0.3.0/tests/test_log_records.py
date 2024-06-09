"""
Burin Log Record Tests

Copyright (c) 2024 William Foster with BSD 3-Clause License
See included LICENSE file for details.
"""

# Python imports
import asyncio
import multiprocessing
import os
from string import Template
import sys
import threading

# Burin import
import burin


# Basic testing values
testLevel = burin.INFO
testLineNumber = 10
testName = "TestRecord"
testPathname = "/test/path"


async def sample_log_record_async():
    """
    Async function to create a generic sample log record.
    """

    return burin.BurinLogRecord(testName, testLevel, testPathname,
                                testLineNumber, "", (), None)


class TestLogRecord:
    """
    Tests log record class.

    .. note::

        Since BurinLogRecord is meant as a base class, and log records act
        partly as a data class for BurinFormatters, most of the class
        functionality is actually tested in subclass and formatter testing.
    """

    def test_get_message(self):
        """
        Tests get message formatting.
        """

        testMessage = "Testing basic log record"
        logRecord = burin.BurinLogRecord(testName, testLevel, testPathname,
                                         testLineNumber, testMessage, (), None)
        assert logRecord.get_message() == testMessage

    def test_log_asyncio_tasks_enabled(self):
        """
        Tests that enabling logAsyncioTasks adds relevant data to record.
        """

        loop = asyncio.new_event_loop()
        try:
            burin.config.logAsyncioTasks = True
            asyncio.set_event_loop(loop)
            asyncRecord = loop.run_until_complete(sample_log_record_async())
        finally:
            loop.close()

        # Tasks names were added in Python 3.8, so the log record getting the
        # task name should quietly fail and remain None
        if hasattr(asyncio.Task, "get_name"):
            assert asyncRecord.taskName is not None
        else:
            assert asyncRecord.taskName is None

    def test_log_asyncio_tasks_disabled(self):
        """
        Tests that disabling logAsyncioTasks adds no data to the record.
        """

        loop = asyncio.new_event_loop()
        try:
            burin.config.logAsyncioTasks = False
            asyncio.set_event_loop(loop)
            asyncRecord = loop.run_until_complete(sample_log_record_async())
        finally:
            loop.close()

        assert asyncRecord.taskName is None

    def test_log_asyncio_tasks_enabled_no_async(self):
        """
        Tests that enabling logAsyncioTasks adds no data if not in async task.
        """

        burin.config.logAsyncioTasks = True
        noneRecord = burin.BurinLogRecord(testName, testLevel, testPathname,
                                          testLineNumber, "", (), None)
        assert noneRecord.taskName is None

    def test_log_asyncio_tasks_disabled_no_async(self):
        """
        Tests that disabling logAsyncioTasks adds no data if not in async task.
        """

        burin.config.logAsyncioTasks = False
        noneRecord = burin.BurinLogRecord(testName, testLevel, testPathname,
                                          testLineNumber, "", (), None)
        assert noneRecord.taskName is None

    def test_log_multiprocessing_enabled(self, monkeypatch):
        """
        Tests that enabling logMultiprocessing adds relevant data to record.
        """

        assert burin.config.logMultiprocessing is True
        testProcessName = "TestProcess"
        with monkeypatch.context() as monkey:
            monkey.setattr(multiprocessing.current_process(), "name",
                           testProcessName)
            mpRecord = burin.BurinLogRecord(testName, testLevel, testPathname,
                                        testLineNumber, "", (), None)
            assert mpRecord.processName == testProcessName

    def test_log_multiprocessing_disabled(self):
        """
        Tests that disabling logMultiprocessing adds no data to the record.
        """

        burin.config.logMultiprocessing = False
        noneRecord = burin.BurinLogRecord(testName, testLevel, testPathname,
                                          testLineNumber, "", (), None)
        assert noneRecord.processName is None

    def test_log_multiprocessing_unavailable(self, monkeypatch):
        """
        Tests when multiprocessing is unavailable (Python issue #8200).
        """

        testProcessName = "TestProcess"

        # Get the module, change the process name, then clear the module
        with monkeypatch.context() as monkey:
            monkey.setattr(multiprocessing.current_process(), "name",
                           testProcessName)
            monkey.setitem(sys.modules, "multiprocessing", None)

            # Set to log multiprocessing and check the record
            burin.config.logMultiprocessing = True
            mpRecord = burin.BurinLogRecord(testName, testLevel, testPathname,
                                            testLineNumber, "", (), None)
            assert mpRecord.processName == "MainProcess"

    def test_log_multiprocessing_exception(self, monkeypatch):
        """
        Tests record for when an exception occurs getting the process name.
        """

        # Overwrite the current_process function to force an exception
        with monkeypatch.context() as monkey:
            monkey.setattr(multiprocessing, "current_process", None)

            # Set to log multiprocessing and check the record
            burin.config.logMultiprocessing = True
            mpRecord = burin.BurinLogRecord(testName, testLevel, testPathname,
                                            testLineNumber, "", (), None)
            assert mpRecord.processName == "MainProcess"

    def test_log_processes_enabled(self):
        """
        Tests that enabling logProcesses adds relevant data to record.
        """

        assert burin.config.logProcesses is True
        expectedPid = os.getpid() if hasattr(os, "getpid") else None
        processRecord = burin.BurinLogRecord(testName, testLevel, testPathname,
                                             testLineNumber, "", (), None)
        assert processRecord.process == expectedPid

    def test_log_processes_disabled(self):
        """
        Tests that disabling logProcesses adds no data to the record.
        """

        burin.config.logProcesses = False
        noneRecord = burin.BurinLogRecord(testName, testLevel, testPathname,
                                          testLineNumber, "", (), None)
        assert noneRecord.process is None

    def test_log_threads_enabled(self):
        """
        Tests that enabling logThreads adds relevant data to record.
        """

        assert burin.config.logThreads is True
        threadRecord = burin.BurinLogRecord(testName, testLevel, testPathname,
                                            testLineNumber, "", (), None)
        assert threadRecord.thread == threading.get_ident()
        assert threadRecord.threadName == threading.current_thread().name

    def test_log_threads_disabled(self):
        """
        Tests that disabling logThreads adds no data to the record.
        """
        burin.config.logThreads = False
        noneRecord = burin.BurinLogRecord(testName, testLevel, testPathname,
                                          testLineNumber, "", (), None)
        assert noneRecord.thread is None
        assert noneRecord.threadName is None

    def test_pathname_invalid(self):
        """
        Tests that an invalid pathname doesn't cause issues.
        """

        invalidPath = 10
        invalidPathRecord = burin.BurinLogRecord(testName, testLevel, invalidPath,
                                                 testLineNumber, "", (), None)
        assert invalidPathRecord.filename == invalidPath
        assert invalidPathRecord.module == "Unknown module"

    def test_repr(self):
        """
        Tests that the custom class representation string is correct.
        """

        testMessage = "Test log message"
        logRecord = burin.BurinLogRecord(testName, testLevel, testPathname,
                                         testLineNumber, testMessage, (), None)
        expectedRepr = (f"<BurinLogRecord: {testName}, {testLevel}, "
                        f"{testPathname}, {testLineNumber}, {testMessage}>")
        assert repr(logRecord) == expectedRepr


class TestPercentLogRecord:
    """
    Tests printf (%) formatting log record class.
    """

    def test_get_message_basic(self):
        """
        Tests get message without formatting.
        """

        testMessage = "Testing percent record"
        logRecord = burin.BurinPercentLogRecord(testName, testLevel,
                                                testPathname, testLineNumber,
                                                testMessage, (), None)
        assert logRecord.get_message() == testMessage

    def test_get_message_args(self):
        """
        Tests get message formatting.
        """

        testMessage = "Testing %s formatting #%d"
        testArgs = ("percent", 1)
        logRecord = burin.BurinPercentLogRecord(testName, testLevel,
                                                testPathname, testLineNumber,
                                                testMessage, testArgs, None)
        assert logRecord.get_message() == testMessage % testArgs

    def test_get_message_args_dict(self):
        """
        Tests get message formatting with a dictionary as the only argument.
        """

        testMessage = "Testing %(msgType)s formatting #%(num)d"
        testArgs = ({"msgType": "percent", "num": 2},)
        logRecord = burin.BurinPercentLogRecord(testName, testLevel,
                                                testPathname, testLineNumber,
                                                testMessage, testArgs, None)
        assert logRecord.get_message() == testMessage % testArgs[0]


class TestBraceLogMessage:
    """
    Tests str.format ({) formatting log record class.
    """

    def test_get_message_basic(self):
        """
        Tests get message without formatting.
        """

        testMessage = "Testing brace record"
        logRecord = burin.BurinBraceLogRecord(testName, testLevel,
                                              testPathname, testLineNumber,
                                              testMessage, (), None)
        assert logRecord.get_message() == testMessage

    def test_get_message_args(self):
        """
        Tests get message formatting with positional arguments.
        """

        testMessage = "Testing {} formatting with {} only #{}"
        testArgs = ("brace", "args", 1)
        logRecord = burin.BurinBraceLogRecord(testName, testLevel,
                                              testPathname, testLineNumber,
                                              testMessage, testArgs, None)
        assert logRecord.get_message() == testMessage.format(*testArgs)

    def test_get_message_kwargs(self):
        """
        Tests get message formatting with keyword arguments.
        """

        testMessage = "Testing {msgStyle} formatting with {argType} only #{num}"
        testKwargs = {"msgStyle": "brace", "argType": "kwargs", "num": 1}
        logRecord = burin.BurinBraceLogRecord(testName, testLevel,
                                              testPathname, testLineNumber,
                                              testMessage, (), None,
                                              **testKwargs)
        assert logRecord.get_message() == testMessage.format(**testKwargs)

    def test_get_message_args_kwargs(self):
        """
        Tests get message formatting with positional and keyword arguments.
        """

        testMessage = "Testing {msgStyle} formatting with {} and {} #{num}"
        testArgs = ("args", "kwargs")
        testKwargs = {"msgStyle": "brace", "num": 1}
        logRecord = burin.BurinBraceLogRecord(testName, testLevel,
                                              testPathname, testLineNumber,
                                              testMessage, testArgs, None,
                                              **testKwargs)
        assert logRecord.get_message() == testMessage.format(*testArgs,
                                                             **testKwargs)

    def test_get_message_args_dict(self):
        """
        Tests get message formatting with a dictionary as the only argument.
        """

        testMessage = "Testing {msgStyle} formatting with {argType} only #{num}"
        testArgs = ({"msgStyle": "brace", "argType": "single dictionary",
                     "num": 1},)
        logRecord = burin.BurinBraceLogRecord(testName, testLevel,
                                              testPathname, testLineNumber,
                                              testMessage, testArgs, None)
        assert logRecord.get_message() == testMessage.format(**testArgs[0])


class TestDollarLogMessage:
    """
    Tests string.Template ($) formatting log record class.
    """

    def test_get_message_basic(self):
        """
        Tests get message without formatting.
        """

        testMessage = "Testing dollar record"
        logRecord = burin.BurinDollarLogRecord(testName, testLevel,
                                               testPathname, testLineNumber,
                                               testMessage, (), None)
        assert logRecord.get_message() == testMessage

    def test_get_message_kwargs(self):
        """
        Tests get message formatting with keyword arguments.
        """

        testMessage = "Testing ${msgStyle} formatting #${num}"
        testKwargs = {"msgStyle": "dollar", "num": 1}
        logRecord = burin.BurinDollarLogRecord(testName, testLevel,
                                               testPathname, testLineNumber,
                                               testMessage, (), None,
                                               **testKwargs)
        assert logRecord.get_message() == Template(testMessage).safe_substitute(testKwargs)

    def test_get_message_args_dict(self):
        """
        Tests get message formatting with a dictionary as the only argument.
        """

        testMessage = "Testing ${msgStyle} formatting with ${argType} only #${num}"
        testArgs = ({"msgStyle": "brace", "argType": "single dictionary",
                     "num": 1},)
        logRecord = burin.BurinDollarLogRecord(testName, testLevel,
                                               testPathname, testLineNumber,
                                               testMessage, testArgs, None)
        assert logRecord.get_message() == Template(testMessage).safe_substitute(testArgs[0])


def test_get_log_record_factory_defaults():
    """
    Tests that the default log record factories are set properly.
    """

    logRecordFactories = {
        "{": burin.BurinBraceLogRecord,
        "$": burin.BurinDollarLogRecord,
        "%": burin.BurinPercentLogRecord
    }

    for factoryKey, factoryClass in logRecordFactories.items():
        assert burin.get_log_record_factory(factoryKey) is factoryClass

def test_get_log_record_factory_none():
    """
    Tests that getting a log record factory with an unknown key returns None.
    """

    assert burin.get_log_record_factory("NOT_A_KEY") is None

def test_make_log_record_from_dict():
    """
    Tests function to make a log record from a dictionary of one.
    """

    testMessage = "Test log message"
    logRecord = burin.BurinLogRecord(testName, testLevel, testPathname,
                                     testLineNumber, testMessage, (), None)

    # Create the dictionary of the record as a handler would when pickling
    recordDict = dict(logRecord.__dict__)
    recordDict["msg"] = logRecord.get_message()
    recordDict["args"] = None
    recordDict["kwargs"] = None
    recordDict["exc_info"] = None
    recordDict.pop("message", None)

    # Check that making a record from the dictionary has the same message
    newRecord = burin.make_log_record(recordDict)
    assert newRecord.get_message() == testMessage


class CustomRecord(burin.BurinLogRecord):
    """
    Test record with fixed message output.
    """
    pass


def test_set_log_record_factory_custom():
    """
    Tests setting a custom log record factory.
    """

    customFactoryKey = "custom"

    burin.set_log_record_factory(CustomRecord, customFactoryKey)

    assert burin.get_log_record_factory(customFactoryKey) is CustomRecord
