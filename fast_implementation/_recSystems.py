'''
Recommender systems abstract classes.
Inspired by sklearn _base.py
'''
#%% Modules
#standard
from abc import ABC, abstractmethod
import numpy as np
import pandas as pd

#personal
from context import likeThr
from fastGraph import Graph


#%% Trivial Recommandation System
class _RecSystem(ABC):
    '''
    Abstract class for recommender systems.
    '''
    def __init__(self):
        pass

    @abstractmethod
    def fit(self, edges):
        pass

    @abstractmethod
    def predict(self, edges, *args):
        pass
    pass



class _Clf(_RecSystem):
    '''
    Classifier recommendation system
    '''
    def __init__(self, df):
        super().__init__()
        self.df = df
        self.set_featFncts()
        pass

    @abstractmethod
    def set_featFncts(self):
        '''Here are defined the features through the use of 'feature functions'.
        A feature function is defined as a function from either the data
        on the user, or the data on the movie, or the data on the edge, to a subset of 
        the real numbers.

        Sets
        -------
        featureFncts: dict of list of functions
            the functions should return a float, corresponding to the extracted feature.
        '''
        self.featFncts = {'user': [],
                      'edge': [],
                      'movie': []
                      }
        pass

    def _get_feature_matrix(self, edges):
        '''
        '''
        df = self.df.iloc[edges]
        featFncts = self.featFncts

        dfByUser = df.groupby('userId')
        dfByMovie = df.groupby('movieId')

        X = pd.DataFrame() 
        X['userId'] = df['userId']
        X['movieId'] = df['movieId']
        X_u = pd.DataFrame(index= df['userId'].drop_duplicates().sort_values())
        X_m = pd.DataFrame(index=  df['movieId'].drop_duplicates().sort_values())

        for k,featFnct in enumerate(featFncts['edge']):
            X['xe'+str(k)] = featFnct(df)

        for k,featFnct in enumerate(featFncts['user']):
            X_u['xu'+str(k)] = featFnct(dfByUser)

        for k,featFnct in enumerate(featFncts['movie']):
            X_m['xm'+str(k)] = featFnct(dfByMovie)

        return X.merge(X_u, on='userId', how='left').merge(X_m, on='movieId', how='left')#.drop(columns=['userId', 'movieId'])

    def _get_labels(self, edges):
        df = self.df.iloc[edges]
        return (df['rating'] > likeThr).astype('uint8')


    @abstractmethod
    def predict(self, edges):
        '''predicts if the user likes the movie, without looking at the score of the edge.
        
        Parameters
        -------
            edges : list
                edges of the sub-graph you consider for the prediction.

        Returns
        -------
            pred: np.array of shape (nUsers,)
                containing the predictions (0 or 1) in the same order
        '''
        pass
    pass
