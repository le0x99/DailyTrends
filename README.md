#  ✨ DailyTrends ✨

# **NOTE** : Overlap-Bug is now fixed and requesting data for multiple keywoards now works fine.
This lightweight API solves the problem of getting only monthly-based data for large time series when collecting Google Trends data. No login required. For unlimited requests, I will implement a Tor-based solution soon.

### Installation

```bash
$ pip install DailyTrends
```




### How to use

```ipython
>>> from DailyTrends.collect import collect_data
# Get the data directly into python.
# The returned dataframe is already indexed and ready for storage/analysis.
>>> data = collect_data("AMD stock",
                    save=False, verbose=False)                   
>>> data.info()

<class 'pandas.core.frame.DataFrame'>
DatetimeIndex: 5666 entries, 2004-01-01 to 2019-07-06
Freq: D
Data columns (total 1 columns):
AMD stock: (Worldwide)    5666 non-null float64
dtypes: float64(1)
memory usage: 88.5 KB

#Plotting some rolling means of the daily data
>>> ax=data.rolling(10).mean().plot();
    data.rolling(25).mean().plot(ax=ax);
    data.rolling(50).mean().plot(ax=ax)
```

![image.png](1.png)

### Add your own data
```ipython
# In this case the actual historic prices of the stock
>>> import pandas as pd
>>> price_data = pd.read_csv("price_data.csv")
>>> merged = pd.merge(price_data, data,
                  left_index=True, right_index=True)
>>> merged[["AMD stock: (Worldwide)", "Open"]].rolling(30).mean().plot()
```
![image.png](2.png)

### Load multiple queries

```ipython
>>> data = collect_data(["Intel", "AMD"],
                   save=False, verbose=False)      
                
```




### To-Do

- Add rescale capabilities
- Optimze multi-query search by combining it to a single request
- Add time range
- Add Tor-Network-based requests
- Add unique identifiers
- Add tqdm
- Prevent Null-Overlaps






## **Disclaimer**

This API is not supported by Google and is for experimental purposes only.


