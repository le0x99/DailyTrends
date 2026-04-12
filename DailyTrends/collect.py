import pandas as pd

from DailyTrends.request import collect_frames
from DailyTrends.rescale import qAggr


def collect_data(
    q: str | list[str],
    start: str = "2004-01-01",
    end: str = "TODAY",
    geo: str = "",
    save: bool = False,
    dest: str | None = None,
    verbose: bool = False,
) -> pd.DataFrame:
    """Collect full-range daily Google Trends data for one or more keywords.

    Parameters
    ----------
    q : str or list[str]
        Search query (single keyword or list of keywords).
    start : str
        Start date in "YYYY-MM-DD" format. Defaults to "2004-01-01".
    end : str
        End date in "YYYY-MM-DD" format or "TODAY". Defaults to "TODAY".
    geo : str
        Geographic region code (e.g. "US", "DE"). Defaults to "" (worldwide).
    save : bool
        If True, save the result as a CSV file.
    dest : str or None
        File path to save CSV to (required if save=True).
    verbose : bool
        If True, print debug information during aggregation.

    Returns
    -------
    pd.DataFrame
        DataFrame with DatetimeIndex and trend values scaled to [0, 100].
    """
    if not isinstance(q, (str, list)):
        raise TypeError(
            "Use a string for single query search or a list of strings "
            "for multiple keywords."
        )
    if isinstance(q, list) and not all(isinstance(item, str) for item in q):
        raise TypeError("All items in the query list must be strings.")

    if save and dest is None:
        raise ValueError("dest must be specified when save=True.")

    # Get the unscaled data pieces
    frames = collect_frames(q, start, end, geo)

    for frame in frames:
        for col in frame:
            frame[col] = frame[col].replace("<1", 1)
            frame[col] = frame[col].astype("int64")

    # Quick-aggregate the data pieces and rescale using overlaps
    df = qAggr(frames, verbose=verbose)

    if save:
        df.to_csv(dest)
    return df
