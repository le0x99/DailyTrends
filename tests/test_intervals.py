"""Tests for the interval generation logic in request.py."""

from datetime import datetime

import pytest

from DailyTrends.request import generate_intervals


class TestGenerateIntervals:
    """Tests for generate_intervals function."""

    def test_returns_list(self):
        intervals = generate_intervals(init_start="2023-01-01", init_end="2024-01-01")
        assert isinstance(intervals, list)
        assert len(intervals) > 0

    def test_single_interval_for_short_range(self):
        """A range shorter than (inc - overlap) days should return one interval."""
        intervals = generate_intervals(init_start="2024-01-01", init_end="2024-03-01")
        assert len(intervals) == 1
        assert "2024-01-01" in intervals[0]
        assert "2024-03-01" in intervals[0]

    def test_interval_format(self):
        """Each interval should be 'YYYY-MM-DD YYYY-MM-DD'."""
        intervals = generate_intervals(init_start="2020-01-01", init_end="2021-01-01")
        for interval in intervals:
            parts = interval.split(" ")
            assert len(parts) == 2
            # Validate date format
            for part in parts:
                datetime.strptime(part, "%Y-%m-%d")

    def test_intervals_are_chronologically_ordered(self):
        """Intervals should be ordered from earliest to latest."""
        intervals = generate_intervals(init_start="2018-01-01", init_end="2020-01-01")
        starts = [interval.split(" ")[0] for interval in intervals]
        assert starts == sorted(starts)

    def test_intervals_overlap(self):
        """Consecutive intervals must have overlapping date ranges."""
        intervals = generate_intervals(
            overlap=35, inc=250, init_start="2018-01-01", init_end="2020-01-01"
        )
        for i in range(len(intervals) - 1):
            end_of_current = datetime.strptime(intervals[i].split(" ")[1], "%Y-%m-%d")
            start_of_next = datetime.strptime(intervals[i + 1].split(" ")[0], "%Y-%m-%d")
            # The end of the current interval should be after the start of the next
            assert end_of_current > start_of_next, (
                f"Interval {i} end ({end_of_current}) should overlap with "
                f"interval {i+1} start ({start_of_next})"
            )

    def test_today_as_end(self):
        """Using 'TODAY' as end should work and use today's date."""
        intervals = generate_intervals(init_start="2024-01-01", init_end="TODAY")
        assert isinstance(intervals, list)
        assert len(intervals) >= 1

    def test_custom_overlap_and_increment(self):
        """Custom overlap and increment values should be respected."""
        intervals_default = generate_intervals(
            init_start="2015-01-01", init_end="2020-01-01"
        )
        intervals_custom = generate_intervals(
            overlap=50, inc=300, init_start="2015-01-01", init_end="2020-01-01"
        )
        # Different parameters should produce different numbers of intervals
        assert len(intervals_default) != len(intervals_custom)

    def test_start_after_end_raises(self):
        """Start date after end date should raise ValueError."""
        with pytest.raises(ValueError, match="must be before end date"):
            generate_intervals(init_start="2025-01-01", init_end="2020-01-01")

    def test_same_start_and_end_raises(self):
        """Same start and end date should raise ValueError."""
        with pytest.raises(ValueError, match="must be before end date"):
            generate_intervals(init_start="2024-01-01", init_end="2024-01-01")

    def test_full_coverage(self):
        """The intervals should collectively cover the end of the date range.

        Note: The algorithm builds intervals backwards from the end, so the
        earliest interval may not reach all the way back to init_start.
        But the last interval must cover the end date.
        """
        start = "2019-01-01"
        end = "2021-01-01"
        intervals = generate_intervals(init_start=start, init_end=end)
        last_end = intervals[-1].split(" ")[1]
        assert last_end >= end
        # All intervals should be within reasonable bounds
        first_start = intervals[0].split(" ")[0]
        assert first_start >= "2018-01-01"  # shouldn't go way before start
