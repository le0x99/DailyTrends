import io
from datetime import datetime
from dateutil.relativedelta import relativedelta as delta
import requests
import urllib
import json
import random
import pandas as pd
import numpy as np
import time
from tqdm import tqdm

def generate_intervals(overlap:int=40,
                       inc:int=265,
                      start:str="2004-01-01") -> list:
    """ 
    start defaults to "2004-01-01", which represents the entire series.
    Format : "YYYY-MM-DD"  
    """
    to_str = lambda dt_date : datetime.strftime(dt_date, "%Y-%m-%d")
    to_dt = lambda str_date : datetime.strptime(str_date, "%Y-%m-%d")
    n_iter = 25
    intervals = []
    for i in range(n_iter):
        start = "2004-01-01" if i == 0 else to_str(to_dt(end) + delta(days=-overlap))
        end = to_str(to_dt(start) + delta(days=+inc))
        intervals.append(start + " " + end)  
    return intervals

def get_frame(q:None, time:str) -> pd.DataFrame:
    q = [q] if type(q) == str else q
    jar = requests.get("https://trends.google.com/").cookies
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
    opener.addheaders = [
    			("Referrer", "https://trends.google.com/trends/explore"),
    			('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.21 (KHTML, like Gecko) Chrome/19.0.1042.0 Safari/535.21'),
    			("Accept", "text/plain") ]
    params_1 = None
    params_0 = {
                            "hl": "en-US",
                            "tz": -120,
                            "req": {
                            "comparisonItem":[{'keyword': query, 'geo': '', 'time': time} for query in q] ,
                                    "category": 0,
                                    "property": "" }}
    params_0["req"] = json.dumps(params_0["req"], separators=(',', ':')) 
    params_0 = urllib.parse.urlencode(params_0)
    params_0 = params_0.replace('%3A', ':').replace('%2C', ',')  
                   
    data = opener.open("https://trends.google.com/trends/api/explore?" + params_0).read().decode('utf8')
    data = data[data.find("{"):]
    data = json.loads(data)
    widgets = data["widgets"]
    
    
    for widget in widgets:
        if widget["title"] == "Interest over time":
            params_1 = {
                                            "req":widget["request"],
                                            "token":widget["token"],
                                            "tz":-120
                                    }
    params_1["req"] = json.dumps(params_1["req"],separators=(',', ':'))
    params_1 = urllib.parse.urlencode(params_1).replace("+", "%20")
    csv_url = 'https://trends.google.com/trends/api/widgetdata/multiline/csv?' + params_1
    result = opener.open(csv_url).read().decode('utf8')
    return pd.read_csv(io.StringIO(result), skiprows=range(0,1), index_col=0, header=0).asfreq("d")

def collect_frames(q:None) -> list:
    intervals = generate_intervals()
    frames = []
    for interval in tqdm(intervals):
        df = get_frame(q, interval)
        time.sleep(random.gammavariate(.99,1.99))
        if len(df) == 0:
            continue
        frames.append(df)
    return frames
