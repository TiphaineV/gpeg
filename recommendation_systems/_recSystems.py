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
    def __init__(self,graph: Graph):
        self.graph = graph
        pass

    @abstractmethod
    def predict_user(self, userId)->int:
        pass

    @abstractmethod
    def predict(self, userArr: np.array)-> np.array:
        pass

    @abstractmethod
    def predict_from_gen(self, gen: GeneratorType):
        pass


class _PredRecSystem(_RecSystem):
    '''
    Class of recommender systems that does not compute probability on each edge.
    '''
    def __init__(self, graph: Graph):
        super().__init__(graph)
        pass

class _ProbaRecSystem(_RecSystem):
    '''
    Class of recommender systems that does compute probability on each edge.
    '''
    def __init__(self, graph: Graph):
        super().__init__(graph)
        pass

    @abstractmethod
    def predict_proba(self, userId : int)->int:
        pass

    @abstractmethod
    def predict_proba_from_gen(self, gen: GeneratorType):
        pass