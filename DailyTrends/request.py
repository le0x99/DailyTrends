import io
import json
import random
import time
import urllib.parse
import urllib.request
from datetime import date, datetime

import pandas as pd
import requests
from dateutil.relativedelta import relativedelta as delta
from tqdm import tqdm


def generate_intervals(
    overlap: int = 35,
    inc: int = 250,
    init_start: str = "2004-01-01",
    init_end: str = "TODAY",
) -> list[str]:
    """Generate overlapping date intervals for Google Trends queries.

    start defaults to "2004-01-01", which represents the entire series.
    Format: "YYYY-MM-DD"
    """

    def to_str(dt_date):
        return datetime.strftime(dt_date, "%Y-%m-%d")

    def to_dt(str_date):
        return datetime.strptime(str_date, "%Y-%m-%d")

    intervals: list[str] = []

    if init_end == "TODAY":
        init_end_dt = to_dt(to_str(date.today()))
    else:
        init_end_dt = to_dt(init_end)
    init_start_dt = to_dt(init_start)

    duration = init_end_dt - init_start_dt
    if duration.days <= 0:
        raise ValueError(
            f"Start date ({init_start}) must be before end date ({init_end})."
        )

    n_iter = int(duration.days / (inc - overlap))
    if n_iter == 0:
        return [to_str(init_start_dt) + " " + to_str(init_end_dt)]

    for i in range(n_iter):
        if i == 0:
            end = to_str(init_end_dt)
            start = to_str(to_dt(end) - delta(days=+inc))
        else:
            last = intervals[i - 1]
            last_start = last[:10]
            end = to_str(to_dt(last_start) + delta(days=+overlap))[:10]
            start = to_str(to_dt(end) - delta(days=+inc))

        intervals.append(start + " " + end)

    intervals.reverse()
    return intervals


def get_frame(q: str | list[str], time_range: str, geo: str) -> pd.DataFrame:
    """Fetch a single Google Trends data frame for the given query and time range."""
    if isinstance(q, str):
        q = [q]

    jar = requests.get("https://trends.google.com/").cookies
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
    opener.addheaders = [
        ("Referrer", "https://trends.google.com/trends/explore"),
        (
            "User-Agent",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        ),
        ("Accept", "text/plain"),
    ]

    params_0 = {
        "hl": "",
        "tz": -120,
        "req": json.dumps(
            {
                "comparisonItem": [
                    {"keyword": query, "geo": geo, "time": time_range} for query in q
                ],
                "category": 0,
                "property": "",
            },
            separators=(",", ":"),
        ),
    }
    params_0_encoded = urllib.parse.urlencode(params_0)
    params_0_encoded = params_0_encoded.replace("%3A", ":").replace("%2C", ",")

    data = (
        opener.open("https://trends.google.com/trends/api/explore?" + params_0_encoded)
        .read()
        .decode("utf8")
    )
    data = data[data.find("{") :]
    data = json.loads(data)
    widgets = data["widgets"]

    params_1 = None
    for widget in widgets:
        if widget["title"] == "Interest over time":
            params_1 = {
                "req": json.dumps(widget["request"], separators=(",", ":")),
                "token": widget["token"],
                "tz": -120,
            }
            break

    if params_1 is None:
        raise ValueError(
            "Could not find 'Interest over time' widget in Google Trends response. "
            "The query may be invalid or Google may have changed their API."
        )

    params_1_encoded = urllib.parse.urlencode(params_1).replace("+", "%20")
    csv_url = (
        "https://trends.google.com/trends/api/widgetdata/multiline/csv?" + params_1_encoded
    )
    result = opener.open(csv_url).read().decode("utf8")
    df = pd.read_csv(
        io.StringIO(result), skiprows=range(0, 1), index_col=0, header=0
    )
    df.index = pd.DatetimeIndex(df.index)
    return df.asfreq("D")


def collect_frames(
    q: str | list[str], start: str, end: str, geo: str
) -> list[pd.DataFrame]:
    """Collect all data frames for the given query across generated intervals."""
    intervals = generate_intervals(init_start=start, init_end=end)
    frames: list[pd.DataFrame] = []
    for interval in tqdm(intervals, desc="Fetching trends data"):
        df = get_frame(q, interval, geo)
        time.sleep(random.gammavariate(0.99, 1.99))
        if len(df) == 0:
            continue
        frames.append(df)
    return frames
