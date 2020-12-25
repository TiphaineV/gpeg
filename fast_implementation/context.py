#%% Modules
import pandas as pd
from functools import reduce
import time

#%% Like Threshold
likeThr = 3.2

#%% Aggregation functions
def agg_as_list(series: pd.Series):
    return [series.iloc[k] for k in range(len(series))]

#%% Processing Data : merging ratings and movies into userData variable shared accross all files
# -- change the filePath here
filePath =  "./"

# -- reading data
userData = pd.read_csv(filePath + 'userData.csv')

# -- basic tests
assert(type(tags['tag'][0]) == list and type(tags['timestamp'][0]) == list) #tester la correspondance si possible aussi
assert(len(userData) == len(ratings))