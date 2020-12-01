'''
Recommender systems abstract classes.
Inspired by sklearn _base.py
'''
#%% Modules
#standard
from abc import ABC, abstractmethod
import numpy as np
from types import GeneratorType

#personal
from node import UserNode, MovieNode
from graph import Graph
from context import ratings, movies, tags


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
    def predict(self, userIds: np.array)-> np.array:
        pass

    @abstractmethod
    def score(self, userIds: np.array, yTrue: np.array):
        pass



class _Clf(_RecSystem):
    '''
    Classifier recommendation system
    '''
    metrics = {
        'precision' : None,
        'recall' : None,
        'f1-score' : None
    }
    def __init__(self):
        super().__init__()
        pass

    def fit(self, edges):
        pass


    @abstractmethod
    def predict(self, userIds: np.array, nRec=1)->np.array:
        '''
        Returns
        -------
            np.array of shape (nUsers, nRec)
        '''
        pass

    def score(self, userNodes : dict, nRec:int, metric= 'precision')-> float:
        '''Not implemented properly
        metric can be precision, recall or f1-score
        '''
        yPred = self.predict(userNodes, nRec) # dim nUsers, nRec
        movies = list(userNodes.values())
        yTrue = [movie.get_likes() for movie in movies]

        # -- precision, only one working atm + not efficient
        count = 0
        for row, likes in enumerate(yTrue):
            for like in likes:
                if like in yPred[row]:
                    count +=1
                    break
        return count / len(yPred)


        '''
        # what it should look like after

        scoreFunc = metrics[metric]
        return scoreFunc(yPred,yTrue)
        '''
    pass