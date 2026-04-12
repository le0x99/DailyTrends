"""Tests for the collect module."""

import pytest

from DailyTrends.collect import collect_data


class TestCollectDataValidation:
    """Tests for input validation in collect_data."""

    def test_invalid_query_type_int(self):
        with pytest.raises(TypeError, match="string for single query"):
            collect_data(123)

    def test_invalid_query_type_none(self):
        with pytest.raises(TypeError, match="string for single query"):
            collect_data(None)

    def test_invalid_query_type_dict(self):
        with pytest.raises(TypeError, match="string for single query"):
            collect_data({"key": "value"})

    def test_list_with_non_strings(self):
        with pytest.raises(TypeError, match="All items"):
            collect_data(["valid", 123])

    def test_save_without_dest(self):
        with pytest.raises(ValueError, match="dest must be specified"):
            collect_data("test", save=True, dest=None)

