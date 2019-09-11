import pandas as pd
import numpy as np
from functools import reduce

from DailyTrends.request import collect_frames
from DailyTrends.rescale import qAggr

def collect_data(q:str,
                 save:bool=False,
                dest:str=None, verbose:bool=False) -> pd.DataFrame:
  if type(q) == str:
    #gets the unscaled data pieces
    frames = collect_frames(q)
    #"quick-aggregates" the data pieces and rescales the values using overlaps
    df = qAggr(frames, verbose=verbose)
    return df if not save else df.to_csv(dest)
  elif type(q) == list:
    return reduce(lambda left,right: pd.merge(left,right,left_index=True, right_index=True),
                  [collect_data(i, save, dest) for i in q])
  else:
    raise TypeError("Use string for single query search / list of strings for multiple keywoards.")
    
    
