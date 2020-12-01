#%% Modules
import pandas as pd
from functools import reduce

#%% Data
filePath =  "../ml-latest-small/"
ratings = pd.read_csv(filePath + "ratings.csv")
movies = pd.read_csv(filePath + "movies.csv")
links = pd.read_csv(filePath + "links.csv")
tags = pd.read_csv(filePath + "tags.csv")
userData = ratings.merge(tags, on= ['userId','movieId'], suffixes= ('_rating','_tag'))
movieData = movies.merge(links, on= ['movieId'])
col = ['userId','movieId','rating','timestamp_rating']


def agg_as_list(series: pd.Series):
    return [series.iloc[k] for k in range(len(series))]

userData = userData.groupby(col, as_index = False).agg(agg_as_list)

