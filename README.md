## DailyTrends

Load the ***entire-daily-worldwide-broad*** time series for any query directly into Python and/or save as csv.


```python
from DailyTrends.collect import collect_data
# Get the data, takes ~1m
data = collect_data("AMD stock", save=False)
data.head()

```
