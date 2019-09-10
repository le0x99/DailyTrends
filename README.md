## DailyTrends

Load the ***entire-daily-worldwide-broad*** time series for any query directly into Python and/or save as csv.


```python
from DailyTrends import get_series
# Get the data, takes 1m
data = get_series("AMD stock", save=False)
data.head()

```
