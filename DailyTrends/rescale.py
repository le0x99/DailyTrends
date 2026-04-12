import logging

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


def aggr(
    x1: pd.DataFrame, x2: pd.DataFrame, verbose: bool = True
) -> pd.DataFrame:
    """Aggregate two overlapping dataframes by computing and applying a rescaling ratio.

    Input: 2 dataframes with exactly 1 column each, datetime-indexed.
    Note: t(x1) << t(x2) — x1 covers an earlier time period than x2.
    """
    # Find common (overlapping) dates
    common = pd.merge(x1, x2, left_index=True, right_index=True)
    if verbose:
        logger.info("Potential ratio points: %d", len(common))

    # Drop Inf, 0, and near-1 values that distort the ratio
    common = common.replace([np.inf, -np.inf, 0, 0.9999], np.nan).dropna()
    if verbose:
        logger.info("Usable ratio points: %d", len(common))

    if len(common) < 1:
        raise ValueError(
            "Ratio could not be calculated — no usable overlap points. "
            "Try a bigger overlap or different time range."
        )

    # Calculate the rescaling ratio
    if len(x1.columns) == 1:
        ratio = (common[common.columns[0]] / common[common.columns[1]]).median()
    else:
        x_col = x1.columns[0] + "_x"
        y_col = x1.columns[0] + "_y"
        ratio = (common[x_col] / common[y_col]).median()

    # Combine: keep x1 as-is, rescale the non-overlapping part of x2
    overlap_index = pd.merge(x1, x2, left_index=True, right_index=True).index
    df = pd.concat([x1, x2.drop(overlap_index) * ratio])

    if ratio > 1:
        return df / max(df[df.columns[0]]) * 100
    return df


def qAggr(frames: list[pd.DataFrame], verbose: bool = True) -> pd.DataFrame:
    """Quick-aggregate n overlapping data pieces into one rescaled dataframe.

    IMPORTANT: input needs to be ordered where
    t(frames[0]) < t(frames[1]) < ... < t(frames[-1])
    """
    if len(frames) == 0:
        raise ValueError("There is no data for this particular query.")
    if len(frames) == 1:
        return frames[0]

    df = aggr(frames[0], frames[1], verbose=verbose)
    for i, x in enumerate(frames[2:], start=2):
        try:
            df = aggr(df, x, verbose=verbose)
        except ValueError:
            logger.warning(
                "Could not aggregate frame %d — skipping (insufficient overlap).", i
            )
            continue
    return df.asfreq("D")
