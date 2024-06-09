"""
Burin Formatter Tests

Copyright (c) 2024 William Foster with BSD 3-Clause License
See included LICENSE file for details.
"""

# Python imports
from string import Template
import time

# PyTest imports
import pytest

# Burin import
import burin


# Basic testing values
testFunction = "test_function"
testLevel = burin.INFO
testLineNumber = 10
testMessage = "This is a log message"
testName = "TestFormatting"
testPathname = "/test/path"
testStackInfo = "Test stack information"


class TestBurinPercentStyle:
    """
    Tests the printf (%) formatter style class.
    """

    def test_validate_valid(self):
        """
        Tests that validation succeeds with a valid format pattern.
        """

        validPattern = "%(asctime)s :: %(message)s"
        validStyle = burin._formatters._percent_style._BurinPercentStyle(validPattern)
        validStyle.validate()

    def test_validate_invalid(self):
        """
        Tests that validation fails with an invalid format pattern.
        """

        invalidPattern = "{asctime} :: {message}"
        invalidStyle = burin._formatters._percent_style._BurinPercentStyle(invalidPattern)
        with pytest.raises(burin.FormatError):
            invalidStyle.validate()

    def test_format_valid(self, basic_record):
        """
        Tests formatting a valid format and record.
        """

        testRecord = basic_record(name=testName, msg=testMessage)
        testRecord.message = testRecord.get_message()
        validPattern = "%(name)s :: %(message)s"
        validStyle = burin._formatters._percent_style._BurinPercentStyle(validPattern)
        testMapping = {"name": testName, "message": testMessage}
        assert validStyle.format(testRecord) == validPattern % testMapping

    def test_format_invalid(self, basic_record):
        """
        Tests formatting an invalid format with a record.
        """

        testRecord = basic_record()
        invalidPattern = "%(name)s :: %(missingField)s :: %(message)s"
        invalidStyle = burin._formatters._percent_style._BurinPercentStyle(invalidPattern)
        with pytest.raises(burin.FormatError):
            invalidStyle.format(testRecord)

    def test_defaults(self, basic_record):
        """
        Tests that defaults mapping is used correctly in formatting.
        """

        testRecord = basic_record(name=testName, msg=testMessage)
        testRecord.message = testRecord.get_message()
        defaultsPattern = "%(name)s :: %(message)s :: %(defaultField)s"
        defaults = {"defaultField": "Fixed value!"}
        style = burin._formatters._percent_style._BurinPercentStyle(defaultsPattern, defaults=defaults)
        fieldValues = {**defaults, "name": testName, "message": testMessage}
        assert style.format(testRecord) == defaultsPattern % fieldValues

    def test_uses_time_true(self):
        """
        Tests uses_time is accurate with time field in format pattern.
        """

        timeFormat = "%(asctime)s :: %(message)s"
        timeStyle = burin._formatters._percent_style._BurinPercentStyle(timeFormat)
        assert timeStyle.uses_time() is True

    def test_uses_time_false(self):
        """
        Tests uses_time is accurate without time field in format pattern.
        """

        noTimeFormat = "%(name)s :: %(message)s"
        noTimeStyle = burin._formatters._percent_style._BurinPercentStyle(noTimeFormat)
        assert noTimeStyle.uses_time() is False


class TestBurinBraceStyle:
    """
    Tests the str.format ({) formatter style class.
    """

    def test_validate_valid(self):
        """
        Tests that validation succeeds with a valid format pattern.
        """

        validPattern = "{asctime} :: {message}"
        validStyle = burin._formatters._brace_style._BurinBraceStyle(validPattern)
        validStyle.validate()

    def test_validate_invalid_no_fields(self):
        """
        Tests that validation fails using an invalid pattern with no fields.
        """

        invalidPattern = "%(asctime)s :: %(message)s"
        invalidStyle = burin._formatters._brace_style._BurinBraceStyle(invalidPattern)
        with pytest.raises(burin.FormatError):
            invalidStyle.validate()

    def test_validate_invalid_field_name(self):
        """
        Tests that validation fails using a pattern with invalid field names.
        """

        invalidPattern = "{;&}"
        invalidStyle = burin._formatters._brace_style._BurinBraceStyle(invalidPattern)
        with pytest.raises(burin.FormatError):
            invalidStyle.validate()

    def test_validate_invalid_conversion(self):
        """
        Tests that validation fails using a pattern with an invalid conversion.
        """

        invalidPattern = "{message!q}"
        invalidStyle = burin._formatters._brace_style._BurinBraceStyle(invalidPattern)
        with pytest.raises(burin.FormatError):
            invalidStyle.validate()

    def test_validate_invalid_specficiation(self):
        """
        Tests that validation fails using an invalid specification.
        """

        invalidPattern = "{message:none}"
        invalidStyle = burin._formatters._brace_style._BurinBraceStyle(invalidPattern)
        with pytest.raises(burin.FormatError):
            invalidStyle.validate()

    def test_format_valid(self, basic_record):
        """
        Tests formatting a valid format and record.
        """

        testRecord = basic_record(name=testName, msg=testMessage)
        testRecord.message = testRecord.get_message()
        validPattern = "{name} :: {message}"
        validStyle = burin._formatters._brace_style._BurinBraceStyle(validPattern)
        testMapping = {"name": testName, "message": testMessage}
        assert validStyle.format(testRecord) == validPattern.format(**testMapping)

    def test_format_invalid(self, basic_record):
        """
        Tests formatting an invalid format with a record.
        """

        testRecord = basic_record()
        invalidPattern = "{name} :: {missingField} :: {message}"
        invalidStyle = burin._formatters._brace_style._BurinBraceStyle(invalidPattern)
        with pytest.raises(burin.FormatError):
            invalidStyle.format(testRecord)

    def test_defaults(self, basic_record):
        """
        Tests that defaults mapping is used correctly in formatting.
        """

        testRecord = basic_record(name=testName, msg=testMessage)
        testRecord.message = testRecord.get_message()
        defaultsPattern = "{name} :: {message} :: {defaultField}"
        defaults = {"defaultField": "Fixed value!"}
        style = burin._formatters._brace_style._BurinBraceStyle(defaultsPattern, defaults=defaults)
        fieldValues = {**defaults, "name": testName, "message": testMessage}
        assert style.format(testRecord) == defaultsPattern.format(**fieldValues)

    def test_uses_time_true(self):
        """
        Tests uses_time is accurate with time field in format pattern.
        """

        timeFormat = "{asctime} :: {message}"
        timeStyle = burin._formatters._brace_style._BurinBraceStyle(timeFormat)
        assert timeStyle.uses_time() is True

    def test_uses_time_false(self):
        """
        Tests uses_time is accurate without time field in format pattern.
        """

        noTimeFormat = "{name} :: {message}"
        noTimeStyle = burin._formatters._brace_style._BurinBraceStyle(noTimeFormat)
        assert noTimeStyle.uses_time() is False


class TestBurinDollarStyle:
    """
    Tests the string.Template ($) formatter style class.
    """

    def test_validate_valid_braced(self):
        """
        Tests that validation succeeds using a pattern with braced fields.
        """

        validPattern = "${asctime} :: ${message}"
        validStyle = burin._formatters._dollar_style._BurinDollarStyle(validPattern)
        validStyle.validate()

    def test_validate_valid_named(self):
        """
        Tests that validation succeeds using a pattern with named fields.
        """

        validPattern = "$asctime :: $message"
        validStyle = burin._formatters._dollar_style._BurinDollarStyle(validPattern)
        validStyle.validate()

    def test_validate_invalid_no_fields(self):
        """
        Tests that validation fails using a pattern with no valid fields.
        """

        invalidPattern = "%(asctime)s :: %(message)s"
        invalidStyle = burin._formatters._dollar_style._BurinDollarStyle(invalidPattern)
        with pytest.raises(burin.FormatError):
            invalidStyle.validate()

    def test_validate_invalid_lone_dollar(self):
        """
        Tests that validation fails with a pattern with a single dollar sign.
        """

        invalidPattern = "$"
        invalidStyle = burin._formatters._dollar_style._BurinDollarStyle(invalidPattern)
        with pytest.raises(burin.FormatError):
            invalidStyle.validate()

    def test_format_valid(self, basic_record):
        """
        Tests formatting a valid format and record.
        """

        testRecord = basic_record(name=testName, msg=testMessage)
        testRecord.message = testRecord.get_message()
        validPattern = "${name} :: ${message}"
        validStyle = burin._formatters._dollar_style._BurinDollarStyle(validPattern)
        testMapping = {"name": testName, "message": testMessage}
        assert validStyle.format(testRecord) == Template(validPattern).substitute(testMapping)

    def test_format_invalid(self, basic_record):
        """
        Tests formatting an invalid format with a record.
        """

        testRecord = basic_record()
        invalidPattern = "${name} :: ${missingField} :: ${message}"
        invalidStyle = burin._formatters._dollar_style._BurinDollarStyle(invalidPattern)
        with pytest.raises(burin.FormatError):
            invalidStyle.format(testRecord)

    def test_defaults(self, basic_record):
        """
        Tests that defaults mapping is used correctly in formatting.
        """

        testRecord = basic_record(name=testName, msg=testMessage)
        testRecord.message = testRecord.get_message()
        defaultsPattern = "${name} :: ${message} :: ${defaultField}"
        defaults = {"defaultField": "Fixed value!"}
        style = burin._formatters._dollar_style._BurinDollarStyle(defaultsPattern, defaults=defaults)
        fieldValues = {**defaults, "name": testName, "message": testMessage}
        assert style.format(testRecord) == Template(defaultsPattern).substitute(fieldValues)

    def test_uses_time_true(self):
        """
        Tests uses_time is accurate with time field in format pattern.
        """

        timeFormat = "${asctime} :: ${message}"
        timeStyle = burin._formatters._dollar_style._BurinDollarStyle(timeFormat)
        assert timeStyle.uses_time() is True

    def test_uses_time_false(self):
        """
        Tests uses_time is accurate without time field in format pattern.
        """

        noTimeFormat = "${name} :: ${message}"
        noTimeStyle = burin._formatters._dollar_style._BurinDollarStyle(noTimeFormat)
        assert noTimeStyle.uses_time() is False


@pytest.fixture
def sample_log_record(basic_record):
    """
    Create a generic log record for formatter testing.
    """

    # Raise a test exception so it has a proper traceback
    testExceptionInfo = None
    try:
        raise Exception("Test exception")
    except Exception as exc:
        testExceptionInfo = (type(exc), exc, exc.__traceback__)

    return basic_record(testName, testLevel, testPathname, testLineNumber,
                        testMessage, (), testExceptionInfo, func=testFunction,
                        sinfo=testStackInfo)


class TestBurinFormatter:
    """
    Tests the Burin log Formatter.
    """

    def test_formatter_invalid_style(self):
        """
        Tests that an exception is raised with an invalid format style.
        """

        with pytest.raises(burin.FormatError):
            burin.BurinFormatter(style="fail")

    def test_formatter_styles_available(self):
        """
        Tests that all of the formatter style options are properly available.
        """

        formatterStyles = {
            "{": burin._formatters._brace_style._BurinBraceStyle,
            "$": burin._formatters._dollar_style._BurinDollarStyle,
            "%": burin._formatters._percent_style._BurinPercentStyle
        }

        for styleKey, styleClass in formatterStyles.items():
            assert isinstance(burin.BurinFormatter(style=styleKey)._style, styleClass)

    def test_formatter_no_validation(self, sample_log_record):
        """
        Tests the a formatter will instantiate and work with no validation.
        """

        # Clear test stack and exception information as it isn't desired here
        sample_log_record.exc_info = None
        sample_log_record.stack_info = None

        recordFormat = "{message}"

        testFormatter = burin.BurinFormatter(recordFormat, style="{", validate=False)

        assert testFormatter.format(sample_log_record) == sample_log_record.msg

    def test_formatter_format_time_default(self, sample_log_record):
        """
        Tests formatting time from a log record using the default time format.
        """

        # Get the log record time into a string based on the default format
        recordCreationTime = time.localtime(sample_log_record.created)
        recordTimeText = time.strftime(burin.BurinFormatter.default_time_format, recordCreationTime)
        recordTimeText += f",{sample_log_record.msecs:0=3.0f}"

        testFormatter = burin.BurinFormatter()

        assert testFormatter.formatTime(sample_log_record) == recordTimeText

    def test_formatter_format_time(self, sample_log_record):
        """
        Tests formatting time from a log record using a custom format.
        """

        dateTimeFormat = "%A %B %d, %I:%M:%S %p"
        recordTimeText = time.strftime(dateTimeFormat, time.localtime(sample_log_record.created))

        testFormatter = burin.BurinFormatter()

        assert testFormatter.formatTime(sample_log_record, dateTimeFormat) == recordTimeText

    def test_formatter_all_fields(self, sample_log_record):
        """
        Tests formatting a record with all fields in the format string.
        """

        # Clear test stack and exception information as it isn't desired here
        sample_log_record.exc_info = None
        sample_log_record.stack_info = None

        dateTimeFormat = "%A %B %d, %I:%M:%S %p"
        recordFormat = ("{asctime} - {created} - {filename} - {funcName} - {levelname} - {levelno} - {lineno} - "
                        "{message} - {module} - {msecs} - {name} - {pathname} - {process} - {processName} - "
                        "{relativeCreated} - {taskName} - {thread} - {threadName}")

        # Get a comparison for the record text
        recordTimeText = time.strftime(dateTimeFormat, time.localtime(sample_log_record.created))
        recordText = recordFormat.format(asctime=recordTimeText, message=sample_log_record.msg,
                                         **sample_log_record.__dict__)

        testFormatter = burin.BurinFormatter(recordFormat, dateTimeFormat, "{")

        assert testFormatter.format(sample_log_record) == recordText

    def test_formatter_defaults(self, sample_log_record):
        """
        Tests formatting defaults are inserted into the message properly.
        """

        # Clear test stack and exception information as it isn't desired here
        sample_log_record.exc_info = None
        sample_log_record.stack_info = None

        formatDefaults = {"test": "Pass"}

        recordText = f"{sample_log_record.msg} :: {formatDefaults['test']}"

        recordFormat = "{message} :: {test}"
        testFormatter = burin.BurinFormatter(recordFormat, style="{", defaults=formatDefaults)

        assert testFormatter.format(sample_log_record) == recordText

    def test_formatter_exception_stack_info(self, sample_log_record):
        """
        Tests formatting a record with exception and stack information.
        """

        # Get the comparison text for the formatted record
        recordText = f"{sample_log_record.msg}"
        recordText += f"\n{burin.BurinFormatter.format_exception(None, sample_log_record.exc_info)}"
        recordText += f"\n{sample_log_record.stack_info}"

        recordFormat = "{message}"
        testFormatter = burin.BurinFormatter(recordFormat, style="{")

        assert testFormatter.format(sample_log_record) == recordText


class TestBurinBufferingFormatter:
    """
    Tests the Burin buffering log formatter.
    """

    def test_buffering_formatter_default_fmt(self):
        """
        Tests that the default formatter is set properly.
        """

        assert burin.BurinBufferingFormatter().linefmt is burin._formatters.formatter._defaultFormatter

    def test_buffering_formatter_fmt(self):
        """
        Tests that the buffering formatter sets a customer formatter properly.
        """

        testFormatter = burin.BurinFormatter()

        assert burin.BurinBufferingFormatter(testFormatter).linefmt is testFormatter
