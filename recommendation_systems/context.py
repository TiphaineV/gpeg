'''
Shared data between all files. 
You might have to change the relative link to the dataset.
'''
#%% Modules
import pandas as pd

#%% Data
# -- relative link to the dataset
filePath =  "../ml-latest-small/"
# -- data shared between files
ratings = pd.read_csv(filePath + "ratings.csv")
movies = pd.read_csv(filePath + "movies.csv")
tags = pd.read_csv(filePath + "tags.csv")
