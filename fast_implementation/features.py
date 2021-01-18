import pandas as pd
import numpy as np

class NodeFeatures:
    def __init__(self):
        pass

    @staticmethod 
    def user_mean(dfByUser:pd.DataFrame):
        return dfByUser['rating'].agg(np.mean)

    @staticmethod 
    def user_corr(dfByUser:pd.DataFrame):
        #-- not working yet
        return dfByUser[['rating', 'movieId']].apply(corr_custom)

    @staticmethod 
    def movie_mean(dfByMovie:pd.DataFrame):
        return dfByMovie['rating'].agg(np.mean)
