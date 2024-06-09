"""
Burin Log Level Tests

Copyright (c) 2024 William Foster with BSD 3-Clause License
See included LICENSE file for details.
"""

# PyTest imports
import pytest

# Burin import
import burin


# Test values
testUnknownInt = 999
testUnknownString = "Unknown"


class TestLogLevels:
    """
    Test log levels and functions.
    """

    def test_default_order(self):
        """
        Tests that the default log levels are still in the correct order.
        """

        assert burin.NOTSET < burin.DEBUG
        assert burin.DEBUG < burin.INFO
        assert burin.INFO < burin.WARNING
        assert burin.WARNING < burin.ERROR
        assert burin.ERROR < burin.CRITICAL

    def test_references(self):
        """
        Tests that the internal log level references are correct.
        """

        for level, name in burin._log_levels._levelToName.items():
            assert burin._log_levels._nameToLevel[name] == level

    def test_get_level_name_default_levels(self):
        """
        Tests the get_level_name function with known values.
        """

        for level, name in burin._log_levels._levelToName.items():
            assert burin.get_level_name(level) == name
            assert burin.get_level_name(name) == level

    def test_names_to_level_mapping(self):
        """
        Tests the get_level_names_mapping function with current values.
        """

        for name, level in burin.get_level_names_mapping().items():
            assert burin._log_levels._nameToLevel[name] == level

    def test_get_level_name_string_case(self):
        """
        Tests the get_level_name function with strings of difference cases.
        """

        assert burin.get_level_name("INFO") == burin.get_level_name("info")

    def test_get_level_name_unassigned(self):
        """
        Tests the get_level_name function with unknown values.
        """

        assert burin.get_level_name(testUnknownInt) == f"Level {testUnknownInt}"
        assert burin.get_level_name(testUnknownString) == f"Level {testUnknownString}"

    def test_check_level_default_levels(self):
        """
        Tests the internal _check_level function with the default levels.
        """

        for level, name in burin._log_levels._levelToName.items():
            assert burin._log_levels._check_level(level) == level
            assert burin._log_levels._check_level(name) == level

    def test_check_level_unknown_int(self):
        """
        Tests the internal _check_level function with an unknown int level.
        """

        assert burin._log_levels._check_level(testUnknownInt) == testUnknownInt

    def test_check_level_unknown_string(self):
        """
        Tests the internal _check_level function with an unknown string level.
        """

        with pytest.raises(ValueError, match=f"Unknown level: '{testUnknownString.upper()}'"):
            burin._log_levels._check_level(testUnknownString)

    def test_check_level_wrong_type(self):
        """
        Tests the internal _check_level function with the wrong data type.
        """

        with pytest.raises(TypeError):
            burin._log_levels._check_level([])
