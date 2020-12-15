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
        pass

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
