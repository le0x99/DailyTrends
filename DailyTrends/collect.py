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

from DailyTrends.request import collect_frames
from DailyTrends.rescale import qAggr

def collect_data(q:str,
                 save:bool=False,
                dest:str=None) -> pd.DataFrame:
  #gets the unscaled data pieces
  frames = collect_frames(q)
  #"quick-aggregates" the data pieces and rescales the values using overlaps
  df = qAggr(frames)
  return df if not save else df.to_csv(dest)
