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
filePath =  "../../ml-latest-small/"

# -- reading data
ratings = pd.read_csv(filePath + "ratings.csv")
movies = pd.read_csv(filePath + "movies.csv")
links = pd.read_csv(filePath + "links.csv")
tags = pd.read_csv(filePath + "tags.csv")

# -- aggregation
col = ['userId','movieId']
tags = tags.groupby(col, as_index = False).agg(agg_as_list)

# -- merging. keeping keys from rating, but bear in mind that some movies are tagged but do not appear in ratings.csv
userData = pd.merge(ratings, tags, on= ['userId','movieId'], suffixes= ('_rating','_tag'), how='left')

# -- basic tests
assert(type(tags['tag'][0]) == list and type(tags['timestamp'][0]) == list) #tester la correspondance si possible aussi
assert(len(userData) == len(ratings))