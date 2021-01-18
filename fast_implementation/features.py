from abc import ABC, abstractmethod
import numpy as np
import numpy.random as rd
import pandas as pd

class StandardFeatures:
    '''
    '''
    def __init__(self):
        pass

    @classmethod
    def get_featFncts(clf):
        featFncts = { 'user' : [],
                      'movie' : []
                      }
        featFncts['user'].append(StandardFeatures.user_mean())
        featFncts['movie'].append(StandardFeatures.movie_mean())
        return featFncts

    @classmethod
    def user_mean(clf):
        def mean(dfByUser:pd.DataFrame):
            return dfByUser['rating'].agg(np.mean)
        return mean

    @classmethod
    def user_corr(clf):
        def corr(dfByUser:pd.DataFrame):
            #-- not working yet
            return dfByUser[['rating', 'movieId']].apply(corr_custom)
        return corr

    @classmethod
    def movie_mean(clf):
        def mean(dfByMovie:pd.DataFrame):
            return dfByMovie['rating'].agg(np.mean)
        return mean

class PreciseFeatures:
    pass