#%% Modules
# standard
from abc import ABC, abstractmethod
import pandas as pd
import numpy.random as rd
from functools import reduce

#personal
from edge import Edge

#%% Hyperparameter
likeThr = 4.0

#%% Node classes
class _Node(ABC):
    '''
    Abstract Class Node
    '''
    def __init__(self, nodeId):
        self.nodeId = nodeId
        self.idxEdges = []
        pass

    def add(self, idxEdge: int):
        '''
        Parameters
        -------
        idxEdge : points towards an edge in the graph
        '''

        self.idxEdges.append(idxEdge)
        pass

    @classmethod
    def set_graph(cls, graph):
        '''every node needs to have the same reference to the graph
        '''
        cls.graph = graph
        pass

    @abstractmethod
    def get_ratings(self):
        return 

    def get_tags(self):
        edges = self.graph.edges
        tagList = [ edges[idx].tag for idx in self.idxEdges ] 
        return reduce(lambda x,y : x + y, tagList)

    def get_avgRating(self):
        edges = self.graph.edges
        degree = self.get_degree()
        avgRating = 0 if degree ==0 else sum(edges[idx].rating for idx in self.idxEdges) / degree
        return avgRating

    def get_degree(self):
        return len(self.idxEdges)

    def get_edges(self, group):
        '''get the edges of the graph from a certain group. 
        Atm group are sets when a split is done. So group can be either 'train' or 'test'.
        '''
        edges = self.graph.edges
        return [edges[idx] for idx in self.idxEdges if edges[idx].group == group]
    pass

class UserNode(_Node):
    def __init__(self, nodeId: int):
        super().__init__(nodeId)
        pass
    
    def get_ratings(self):
        edges = self.graph.edges
        return {edges[idx].movieId : edges[idx].rating for idx in self.idxEdges}

    def get_likes(self):
        '''get the movies that the user likes. It is controled by the HP likeThr.
        '''
        edges = self.graph.edges
        return [edges[idx].movieId for idx in self.idxEdges if edges[idx].rating >= likeThr]

    pass

class MovieNode(_Node):
    def __init__(self, nodeId: int):
        super().__init__(nodeId)
        pass

    def get_ratings(self):
        edges = self.graph.edges
        return {edge[idx].userId : edge[idx].ratings for idx in self.idxEdges}
    pass
