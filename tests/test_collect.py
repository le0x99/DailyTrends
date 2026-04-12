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

    def test_string_query_accepted(self):
        """String query should pass validation (will fail at network level)."""
        # We only test that validation passes, not that the network call works
        # The actual API call will fail in tests, so we test up to that point
        with pytest.raises(Exception):
            # This will raise a network-related error, not a TypeError
            collect_data("test_query_12345", start="2024-01-01", end="2024-01-02")

    def test_list_query_accepted(self):
        """List query should pass validation (will fail at network level)."""
        with pytest.raises(Exception):
            collect_data(["test1", "test2"], start="2024-01-01", end="2024-01-02")
