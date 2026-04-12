"""Tests for the request module's get_frame and collect_frames functions."""

import json
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from DailyTrends.request import get_frame


class TestGetFrame:
    """Tests for the get_frame function."""

    def _mock_explore_response(self, queries):
        """Build a mock Google Trends explore API response."""
        widget_request = {
            "time": "2024-01-01 2024-03-01",
            "requestOptions": {"property": "", "backend": "IZG"},
        }
        payload = {
            "widgets": [
                {
                    "title": "Interest over time",
                    "request": widget_request,
                    "token": "fake_token_123",
                },
                {"title": "Interest by region", "request": {}, "token": "other"},
            ]
        }
        return ")]}'\n" + json.dumps(payload)

    def _mock_csv_response(self, queries):
        """Build a mock CSV response for multiline data."""
        if isinstance(queries, str):
            queries = [queries]
        header = "Day," + ",".join(queries)
        rows = [
            "2024-01-01," + ",".join(["50"] * len(queries)),
            "2024-01-02," + ",".join(["60"] * len(queries)),
            "2024-01-03," + ",".join(["70"] * len(queries)),
        ]
        return "\n".join([header] + rows)

    @patch("DailyTrends.request.urllib.request.build_opener")
    @patch("DailyTrends.request.requests.get")
    def test_single_query(self, mock_requests_get, mock_build_opener):
        """Test fetching data for a single query."""
        mock_requests_get.return_value = MagicMock(cookies={})

        mock_opener = MagicMock()
        mock_build_opener.return_value = mock_opener

        query = "python"
        explore_resp = self._mock_explore_response(query)
        csv_resp = self._mock_csv_response(query)

        mock_opener.open.side_effect = [
            MagicMock(read=MagicMock(return_value=explore_resp.encode("utf8"))),
            MagicMock(read=MagicMock(return_value=csv_resp.encode("utf8"))),
        ]

        df = get_frame(query, "2024-01-01 2024-01-03", geo="")
        assert isinstance(df, pd.DataFrame)
        assert isinstance(df.index, pd.DatetimeIndex)

    @patch("DailyTrends.request.urllib.request.build_opener")
    @patch("DailyTrends.request.requests.get")
    def test_missing_widget_raises(self, mock_requests_get, mock_build_opener):
        """If 'Interest over time' widget is missing, should raise ValueError."""
        mock_requests_get.return_value = MagicMock(cookies={})

        mock_opener = MagicMock()
        mock_build_opener.return_value = mock_opener

        payload = {"widgets": [{"title": "Something else", "request": {}, "token": "x"}]}
        explore_resp = ")]}'\n" + json.dumps(payload)

        mock_opener.open.return_value = MagicMock(
            read=MagicMock(return_value=explore_resp.encode("utf8"))
        )

        with pytest.raises(ValueError, match="Interest over time"):
            get_frame("test", "2024-01-01 2024-03-01", geo="")

    @patch("DailyTrends.request.urllib.request.build_opener")
    @patch("DailyTrends.request.requests.get")
    def test_list_query(self, mock_requests_get, mock_build_opener):
        """Test fetching data for multiple queries as a list."""
        mock_requests_get.return_value = MagicMock(cookies={})

        mock_opener = MagicMock()
        mock_build_opener.return_value = mock_opener

        queries = ["python", "java"]
        explore_resp = self._mock_explore_response(queries)
        csv_resp = self._mock_csv_response(queries)

        mock_opener.open.side_effect = [
            MagicMock(read=MagicMock(return_value=explore_resp.encode("utf8"))),
            MagicMock(read=MagicMock(return_value=csv_resp.encode("utf8"))),
        ]

        df = get_frame(queries, "2024-01-01 2024-01-03", geo="")
        assert isinstance(df, pd.DataFrame)
        assert len(df.columns) == len(queries)

    @patch("DailyTrends.request.urllib.request.build_opener")
    @patch("DailyTrends.request.requests.get")
    def test_string_query_converted_to_list(self, mock_requests_get, mock_build_opener):
        """A string query should be wrapped in a list internally."""
        mock_requests_get.return_value = MagicMock(cookies={})

        mock_opener = MagicMock()
        mock_build_opener.return_value = mock_opener

        explore_resp = self._mock_explore_response("test")
        csv_resp = self._mock_csv_response("test")

        mock_opener.open.side_effect = [
            MagicMock(read=MagicMock(return_value=explore_resp.encode("utf8"))),
            MagicMock(read=MagicMock(return_value=csv_resp.encode("utf8"))),
        ]

        # Should not raise — string gets wrapped to list internally
        df = get_frame("test", "2024-01-01 2024-01-03", geo="")
        assert isinstance(df, pd.DataFrame)
