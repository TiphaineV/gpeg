#%% Modules
import pandas as pd
from functools import reduce

#%% Aggregation functions
def agg_as_list(series: pd.Series):
    return [series.iloc[k] for k in range(len(series))]

#%% Processing Data : merging ratings and movies into userData variable shared accross all files
# -- change the filePath here
filePath =  "../ml-latest-small/" 

# -- reading data
ratings = pd.read_csv(filePath + "ratings.csv")
movies = pd.read_csv(filePath + "movies.csv")
links = pd.read_csv(filePath + "links.csv")
tags = pd.read_csv(filePath + "tags.csv")

# -- merging
userData = ratings.merge(tags, on= ['userId','movieId'], suffixes= ('_rating','_tag'))
movieData = movies.merge(links, on= ['movieId'])
col = ['userId','movieId','rating','timestamp_rating']

# -- aggregation decreases number of rows
userData = userData.groupby(col, as_index = False).agg(agg_as_list)

