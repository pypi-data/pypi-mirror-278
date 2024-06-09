"""
Burin Stream Handler Tests

Copyright (c) 2024 William Foster with BSD 3-Clause License
See included LICENSE file for details.
"""

# Python imports
import io
import inspect
import sys

# Burin imports
import burin


class TestStreamHandler:
    """
    Tests the stream handler class.

    Since the BurinStreamHandler class subclasses and uses the standard library
    :class:`logging.StreamHandler` for most of its functionality only the parts
    of the class implemented directly in Burin are tested.
    """

    def test_default_stream(self, basic_stream_handler):
        """
        Tests that the default stream is set correctly.
        """

        defaultHandler = basic_stream_handler()

        assert defaultHandler.stream is sys.stderr

    def test_set_stream_different(self, basic_stream_handler, basic_record):
        """
        Tests that setting the stream to a different stream works.
        """

        logStreamA = io.StringIO()
        logMessageA = "Test log message: A"
        logRecordA = basic_record(msg=logMessageA)

        setHandler = basic_stream_handler(logStreamA)
        setHandler.handle(logRecordA)

        logStreamA.seek(0)
        assert logStreamA.read() == f"{logMessageA}\n"

        logStreamB = io.StringIO()
        logMessageB = "Test log message: B"
        logRecordB = basic_record(msg=logMessageB)

        # Ensure the handler returns the original stream
        assert setHandler.set_stream(logStreamB) is logStreamA

        setHandler.handle(logRecordB)
        logStreamB.seek(0)
        assert logStreamB.read() == f"{logMessageB}\n"

    def test_set_stream_same(self, basic_stream_handler, basic_record):
        """
        Tests that setting the stream to the same stream works.
        """

        logStream = io.StringIO()
        logMessageA = "Test log message: A"
        logRecordA = basic_record(msg=logMessageA)
        logMessageB = "Test log message: B"
        logRecordB = basic_record(msg=logMessageB)

        setHandler = basic_stream_handler(logStream)
        setHandler.handle(logRecordA)

        logStream.seek(0)
        assert logStream.read() == f"{logMessageA}\n"

        # None should be returned if not replacing a stream
        assert setHandler.set_stream(logStream) is None

        setHandler.handle(logRecordB)
        logStream.seek(0)
        assert logStream.read() == f"{logMessageA}\n{logMessageB}\n"

    def test_set_level_init(self, basic_stream_handler):
        """
        Tests setting the log level through class initialization.
        """

        defaultLevel = inspect.signature(burin.BurinStreamHandler).parameters["level"]

        newLevel = burin.INFO if defaultLevel != burin.INFO else burin.DEBUG

        levelHandler = basic_stream_handler(level=newLevel)

        assert levelHandler.level == newLevel

    def test_repr(self, basic_stream_handler):
        """
        Tests that the handler class representation string is correct.
        """

        # Check based on default level
        reprHandler = basic_stream_handler()
        streamName = str(getattr(reprHandler.stream, "name", ""))
        streamName += " "

        assert repr(reprHandler) == f"<BurinStreamHandler {streamName}(NOTSET)>"
