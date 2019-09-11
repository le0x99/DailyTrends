import pandas as pd
import numpy as np   

def aggr(x1:pd.DataFrame,
         x2:pd.DataFrame, verbose:bool=False) -> pd.DataFrame:
    """ Input 2 dataframes with exactly 1 column, which is indexed."""
    """ Note : t(x1) << t(x2)"""
    #Find common
    common = pd.merge(x1, x2, left_index=True, right_index=True)
    print("Potential Ratio Points : ", len(common)) if verbose else None
    #Drop Inf and 0
    common = common.replace([np.inf, -np.inf, 0], np.nan).dropna()
    print("Usable Ratio Points : ", len(common)) if verbose else None
    if len(common) < 1:
        raise ValueError("Ratio could not be calculated, try bigger overlap.")
    #Calc Ratio
    common["ratio"] = common[common.columns[0]] / common[common.columns[1]]
    ratio = common["ratio"].value_counts().idxmax()
    df = x1.append(x2.drop(pd.merge(x1, x2, left_index=True, right_index=True).index)*ratio)
    return df/max(df[df.columns[0]])*100 if ratio > 1 else df

def qAggr(frames:list, verbose:bool=False) -> pd.DataFrame:
    """convienent function to quick-aggregate n data pieces"""
    """IMPORTANT : input needs to be ordered where t(args[0]) < t(args[1]) < ... < t(args[-1])"""
    df = aggr(frames[0], frames[1], verbose=verbose)
    for x in frames[2:]:
        df = aggr(df, x, verbose=verbose)
    return df.asfreq("D")
