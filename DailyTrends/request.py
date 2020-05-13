import io
from datetime import datetime, date
from dateutil.relativedelta import relativedelta as delta
import requests
import urllib
import json
import random
import pandas as pd
import numpy as np
import time
from tqdm import tqdm

def generate_intervals(overlap:int=35,
                       inc:int=250,
                      init_start:str="2004-01-01", init_end:str="TODAY") -> list:
    """ 
    start defaults to "2004-01-01", which represents the entire series.
    Format : "YYYY-MM-DD"  
    """
    to_str = lambda dt_date : datetime.strftime(dt_date, "%Y-%m-%d")
    to_dt = lambda str_date : datetime.strptime(str_date, "%Y-%m-%d")
    intervals = []
    if init_end == "TODAY":
        init_end = to_dt(to_str(date.today()))
    else:
        init_end = to_dt(init_end)
    init_start = to_dt(init_start)
    duration = init_end - init_start
    n_iter = int(duration.days / (inc - overlap))
    if n_iter == 0:
        return [to_str(init_start) + " " + to_str(init_end)]
    for i in range(n_iter):
        # Start(i) < End(i-1)
        # End(i) > Start(i+1)
        if i == 0:
            end = to_str(init_end)
            start = to_str(to_dt(end) - delta(days=+inc))
        else:
            last = intervals[i-1]
            last_start, last_end = last[:10], last[11:]
            end = to_str(to_dt(last_start) + delta(days=+overlap))[:10]
            start = to_str(to_dt(end) - delta(days=+inc))
            
        intervals.append(start + " " + end)
        
    intervals.reverse()
    return intervals

def get_frame(q:None, time:str, geo:str) -> pd.DataFrame:
    q = [q] if type(q) == str else q
    jar = requests.get("https://trends.google.com/").cookies
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
    opener.addheaders = [
    			("Referrer", "https://trends.google.com/trends/explore"),
    			('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.21 (KHTML, like Gecko) Chrome/19.0.1042.0 Safari/535.21'),
    			("Accept", "text/plain") ]
    params_1 = None
    params_0 = {
                            "hl": "",
                            "tz": -120,
                            "req": {
                            "comparisonItem":[{'keyword': query, 'geo': geo, 'time': time} for query in q] ,
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

def collect_frames(q:None, start:str, end:str, geo:str) -> list:
    intervals = generate_intervals(init_start=start, init_end=end)
    frames = []
    for interval in tqdm(intervals):
    
        df = get_frame(q, interval, geo)
        #print(len(df))
        time.sleep(random.gammavariate(.99,1.99))
        if len(df) == 0:
            continue
        frames.append(df)
    return frames
