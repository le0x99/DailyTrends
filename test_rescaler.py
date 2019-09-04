
import numpy as np
import pandas as pd
import random
from rescaler import aggr, qAggr
from IPython.display import display_html


### Create toy dfs to check consistency of the rescaler

# draws random numbers with a weight on zeros, since they occure pretty often in the trends data
def drawer() -> int:
    return random.choice([0] * 100 + list(np.random.randint(0, 10_000,
                         dtype="int",
                         size=1000))  )
 #toy df   
df = pd.DataFrame({"x" : [ drawer() for _ in range(284)]},
                          index = pd.date_range(start="1/1/2004", end="10/10/2004", freq="d"))

#MaxScale the frames
MaxScale = lambda _ : (_/_.values.max() * 100)

scaled_df = MaxScale(df)

# Slice the df into 4 overlapping pieces and scale them into [0, 100]
frac = int(len(df)/4)
ol = 20 #overlap
a, b = MaxScale(df[:frac+ol]), MaxScale(df[frac:frac*2+ol])
c, d = MaxScale(df[frac*2: frac*3+ol]), MaxScale(df[frac*3:])

rescaled_df = qAggr([a, b, c, d])

check = pd.DataFrame({"true" : df.x.values, 
              "scaled" : scaled_df.x.values,
              "rescaled" : rescaled_df.x.values })



