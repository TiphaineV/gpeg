'''
Recommender systems abstract classes.
Inspired by sklearn _base.py
'''
#%% Modules
#standard
from abc import ABC, abstractmethod
import numpy as np

#personal
from node import UserNode, MovieNode
from context import userData
from fastGraph import _Graph


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
    def __init__(self):
        super().__init__()
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
        '''Only user and movie features implemented yet
        '''
        featFncts = self.featFncts
        userNodes = _Graph.group_by_user(edges)
        movieNodes = _Graph.group_by_movie(edges)

        X = [] # the feature matrix
        for edge in edges:
            userFeat = userNodes[edge.userId].get_features(featFncts['user'])
            movieFeat = movieNodes[edge.movieId].get_features(featFncts['movie'])
            edgeFeat = edge.get_features(featFncts['edge'])

            v = np.concatenate((userFeat, edgeFeat, movieFeat))
            X.append(v)
            if len(v) == 0:
                raise ValueError('No feature for the edge: ', edge.userId, edge.movieId)

        return np.stack(X, axis= 0)


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
