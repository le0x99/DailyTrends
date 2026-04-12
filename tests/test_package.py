"""Tests for package-level attributes and imports."""

import DailyTrends


class TestPackage:
    def test_version(self):
        assert DailyTrends.__version__ == "6.0.0"

    def test_collect_data_importable(self):
        assert callable(DailyTrends.collect_data)

    def test_all_exports(self):
        assert "collect_data" in DailyTrends.__all__
        assert "__version__" in DailyTrends.__all__

    def test_submodule_imports(self):
        from DailyTrends.collect import collect_data
        from DailyTrends.request import collect_frames, generate_intervals, get_frame
        from DailyTrends.rescale import aggr, qAggr

        assert callable(generate_intervals)
        assert callable(get_frame)
        assert callable(collect_frames)
        assert callable(aggr)
        assert callable(qAggr)
        assert callable(collect_data)
