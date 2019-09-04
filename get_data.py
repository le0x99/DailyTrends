#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 14:19:57 2019

@author: Leonard
"""

import io
from datetime import datetime
from dateutil.relativedelta import relativedelta as delta
import requestsx
import urllib
import json
import random
import pandas as pd
import numpy as np
import time

from torrequest import TorRequest
tr=TorRequest(password='<unhashed_password>')

def generate_intervals(overlap:int=20, inc:int=265) -> list:
    to_str = lambda dt_date : datetime.strftime(dt_date, "%Y-%m-%d")
    to_dt = lambda str_date : datetime.strptime(str_date, "%Y-%m-%d")
    n_iter = 23
    intervals = []
    start = "2004-01-01"
    for i in range(n_iter):
        start = "2004-01-01" if i == 0 else to_str(to_dt(end) + delta(days=-overlap))
        end = to_str(to_dt(start) + delta(days=+inc))
        intervals.append(start + " " + end)  
    return intervals
        

def get_frame(q:str, time:str) -> pd.DataFrame:
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
                            "comparisonItem": [
                                    {
                                            "keyword": q,
                                            "geo":"",
                                            "time": time
                                    }
                                    ],
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
    return pd.read_csv(io.StringIO(result), skiprows=range(0,1), index_col=0, header=0)

def collect_frames(q:str) -> list:
    intervals = generate_intervals()
    frames = []
    for interval in intervals:
        df = get_frame(q, interval)
        time.sleep(random.gammavariate(.99,1.99))
        if len(df) == 0:
            continue
        frames.append(df)
    return frames

frames = collect_frames("clinuvel")


def aggr(x1, x2):
    """ Input 2 dataframes with exactly 1 column, which is indexed."""
    """ Note : t(x1) << t(x2)"""
    #Find common
    common = pd.merge(x1, x2, left_index=True, right_index=True)
    print("Potential Ratio Points : ", len(common))
    #Drop Inf and 0
    common = common.replace([np.inf, -np.inf, 0], np.nan).dropna()
    print("Usable Ratio Points : ", len(common))
    if len(common) < 1:
        raise ValueError("Ratio could not be calculated, try bigger overlap.")
    #Calc Ratio
    common["ratio"] = common[common.columns[0]] / common[common.columns[1]]
    ratio = common["ratio"].value_counts().idxmax()
    df = x1.append(x2.drop(pd.merge(x1, x2, left_index=True, right_index=True).index)*ratio)
    if ratio > 1:
        return df/max(df[df.columns[0]])*100
    return df

def qAggr(*args):
    """convienent function to multi-aggregate n data pieces"""
    """IMPORTANT : input needs to be ordered where t(args[0]) < t(args[1]) < ... < t(args[-1])"""
    df = aggr(args[0], args[1])
    for x in args[2:]:
        df = aggr(df, x)
    return df

from IPython.display import display_html
def display_side_by_side(*args):
    html_str=''
    for df in args:
        html_str+=df.to_html()
    display_html(html_str.replace('table','table style="display:inline"'),raw=True)
            
        
    

