"""
Burin Filter Tests

Copyright (c) 2024 William Foster with BSD 3-Clause License
See included LICENSE file for details.
"""

# PyTest imports
import pytest

# Burin import
import burin


# Basic testing values
testLevel = burin.INFO
testLineNumber = 10
testMessage = "This is a log message"
testPathname = "/test/path"

# Names for the test log records to create the hierarchy
childName = "A.B"
grandchildName = "A.B.C"
parentName = "A"
siblingName = "A.BB"
similarName = "AA"

@pytest.fixture
def parent_record(basic_record):
    """
    Creates a log record that would by at the top of a hierarchy.
    """

    return basic_record(parentName)

@pytest.fixture
def child_record(basic_record):
    """
    Creates a log record that is a child of a parent in the hierarchy.
    """

    return basic_record(childName)

@pytest.fixture
def grandchild_record(basic_record):
    """
    Creates a log record that is a grandchild of a parent in the hierarchy.
    """

    return basic_record(grandchildName)

@pytest.fixture
def sibling_record(basic_record):
    """
    Creates a log record that is a sibling of a child in the hierarchy.
    """

    return basic_record(siblingName)

@pytest.fixture
def similar_record(basic_record):
    """
    Creates a log record that is a similar to the parent in the hierarchy.
    """

    return basic_record(similarName)

@pytest.fixture
def empty_filter():
    """
    Creates a filter that allows all records.
    """

    return burin.BurinFilter()

@pytest.fixture
def parent_filter():
    """
    Creates a filter that only allows a parent and lower hierarchical records.
    """

    return burin.BurinFilter(parentName)

@pytest.fixture
def child_filter():
    """
    Creates a filter that only allows a child and lower hierarchical records.
    """

    return burin.BurinFilter(childName)


class TestFilter:
    """
    Tests the default filter class.
    """

    def test_empty_filter(self, empty_filter, parent_record, child_record,
                          grandchild_record, sibling_record, similar_record):
        """
        Tests that an empty filter string allows any log record.
        """

        assert empty_filter.filter(parent_record) is True
        assert empty_filter.filter(child_record) is True
        assert empty_filter.filter(grandchild_record) is True
        assert empty_filter.filter(sibling_record) is True
        assert empty_filter.filter(similar_record) is True

    def test_parent_filter(self, parent_filter, parent_record, child_record,
                           grandchild_record, sibling_record, similar_record):
        """
        Tests filtering records at the parent level.
        """

        assert parent_filter.filter(parent_record) is True
        assert parent_filter.filter(child_record) is True
        assert parent_filter.filter(grandchild_record) is True
        assert parent_filter.filter(sibling_record) is True
        assert parent_filter.filter(similar_record) is False

    def test_child_filter(self, child_filter, parent_record, child_record,
                          grandchild_record, sibling_record, similar_record):
        """
        Tests filtering records at the child level.
        """

        assert child_filter.filter(parent_record) is False
        assert child_filter.filter(child_record) is True
        assert child_filter.filter(grandchild_record) is True
        assert child_filter.filter(sibling_record) is False
        assert child_filter.filter(similar_record) is False


class TestFilterer:
    """
    Tests the filterer base class used for loggers and handlers.
    """

    def test_add_filter(self, basic_filterer, empty_filter, parent_filter,
                        child_filter):
        """
        Tests adding multiple filters.
        """

        testFilters = [empty_filter, parent_filter, child_filter]
        addfilterer = basic_filterer()

        for eachFilter in testFilters:
            addfilterer.add_filter(eachFilter)

        assert len(addfilterer.filters) == len(testFilters)

        for i in range(len(testFilters)):
            assert addfilterer.filters[i] is testFilters[i]

    def test_readd_filter(self, basic_filterer, empty_filter):
        """
        Tests that re-adding the same filter doesn't duplicate it in the list.
        """

        reAddfilterer = basic_filterer()

        reAddfilterer.add_filter(empty_filter)
        reAddfilterer.add_filter(empty_filter)

        assert len(reAddfilterer.filters) == 1
        assert reAddfilterer.filters[0] is empty_filter

    def test_remove_filter(self, basic_filterer, empty_filter, parent_filter,
                           child_filter):
        """
        Tests removing a filter.
        """

        testFilters = [empty_filter, parent_filter, child_filter]
        removefilterer = basic_filterer()

        for eachFilter in testFilters:
            removefilterer.add_filter(eachFilter)

        assert len(removefilterer.filters) == len(testFilters)

        removefilterer.remove_filter(parent_filter)

        assert len(removefilterer.filters) == (len(testFilters) - 1)
        assert parent_filter not in removefilterer.filters

    def test_remove_non_present_filter(self, basic_filterer, empty_filter,
                                       parent_filter):
        """
        Tests removing a filter not in filter list doesn't impact the list.
        """

        removefilterer = basic_filterer()

        removefilterer.add_filter(empty_filter)
        removefilterer.remove_filter(parent_filter)

        assert len(removefilterer.filters) == 1
        assert removefilterer.filters[0] is empty_filter

    def test_single_filter_checks(self, basic_filterer, parent_filter,
                                  parent_record, child_record,
                                  grandchild_record, sibling_record,
                                  similar_record):
        """
        Tests a single filter check with different records.
        """

        checkFilterer = basic_filterer()

        checkFilterer.add_filter(parent_filter)

        assert checkFilterer.filter(parent_record) is parent_record
        assert checkFilterer.filter(child_record) is child_record
        assert checkFilterer.filter(grandchild_record) is grandchild_record
        assert checkFilterer.filter(sibling_record) is sibling_record
        assert checkFilterer.filter(similar_record) is False

    def test_multi_filter_checks(self, basic_filterer, parent_filter,
                                 child_filter, parent_record, child_record,
                                 grandchild_record, sibling_record,
                                 similar_record):
        """
        Tests multiple filter checks with different records.
        """

        checkFilterer = basic_filterer()

        checkFilterer.add_filter(parent_filter)
        checkFilterer.add_filter(child_filter)

        assert checkFilterer.filter(parent_record) is False
        assert checkFilterer.filter(child_record) is child_record
        assert checkFilterer.filter(grandchild_record) is grandchild_record
        assert checkFilterer.filter(sibling_record) is False
        assert checkFilterer.filter(similar_record) is False

    def test_modifying_filters(self, basic_filterer, parent_record,
                               line_increment_filter):
        """
        Tests that modified records are returned through the filter process.
        """

        modifyingFilterer = basic_filterer()

        # Use two filters to ensure the record is progressively modified.
        modifyingFilterer.add_filter(line_increment_filter())
        modifyingFilterer.add_filter(line_increment_filter())

        alteredRecord = modifyingFilterer.filter(parent_record)

        assert alteredRecord is not parent_record
        assert alteredRecord.lineno == (parent_record.lineno + 2)
