import pandas as pd
import numpy as np

from DailyTrends.request import collect_frames
from DailyTrends.rescale import qAggr

def collect_data(q:None,
                 save:bool=False,
                dest:str=None, verbose:bool=False) -> pd.DataFrame:
    if type(q) != str and type(q) != list:
        raise TypeError("Use string for single query search / list of strings for multiple keywoards.")
    #gets the unscaled data pieces
    frames = collect_frames(q)
    #"quick-aggregates" the data pieces and rescales the values using overlaps
    df = qAggr(frames, verbose=verbose)
    return df if not save else df.to_csv(dest)
