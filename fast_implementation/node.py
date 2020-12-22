#%% Modules
# standard
from abc import ABC, abstractmethod
import pandas as pd
import numpy.random as rd
from functools import reduce
import numpy as np

#personal
from edge import Edge

#%% Hyperparameter
likeThr = 3.0

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

    def hide(self, nHide):
        '''randomly hides nHide edges of the node

        Returns
        -------
            The hidden edges as a list
        '''
        idxEdges = self.idxEdges
        rd.shuffle(idxEdges)
        return self.graph.hide_edges(idxEdges[:nHide])


    @classmethod
    def set_graph(cls, graph):
        '''every node needs to have the same reference to the graph
        '''
        cls.graph = graph
        pass

    @abstractmethod
    def get_ratings(self):
        return 

    @abstractmethod
    def get_tags(self):
        return

    def all_tags(self):
        edges = self.graph.edges
        tagList = [ edges[idx].tag for idx in self.idxEdges ] 
        return reduce(lambda x,y : x + y, tagList)

    @abstractmethod
    def get_features(self, fncts: list):
        '''Extract features from the node
        '''
        return

    def get_avgRating(self):
        edges = self.graph.edges
        degree = self.get_degree()
        avgRating = 0 if degree == 0 else sum(edges[idx].rating for idx in self.idxEdges) / degree
        return avgRating

    def get_degree(self):
        return len(self.idxEdges)

    def get_edges(self, group):
        '''edges of the graph from a certain group. 
        Atm group are sets when a split is done. So group can be either 'train' or 'test'.
        '''
        edges = self.graph.edges
        return [edges[idx] for idx in self.idxEdges if edges[idx].group == group]
    pass

class UserNode(_Node):
    def __init__(self, nodeId: int):
        super().__init__(nodeId)
        pass

    def __str__(self):
        return str(self.get_labels())


    def hide_labels(self, nHide)-> list:
        '''hides randomly some labels of the node.

        Returns
        -------
            The hidden edges as a list
        '''
        idxLabels = self._get_idxLabels()
        rd.shuffle(idxLabels)
        return self.graph.hide_edges(idxLabels[:nHide])

    def _get_idxLabels(self)->list:
        '''Among the references to the edges in the graph, returns the ones that 
        points towards liked movies, which are the labels of the rec system seen as
        a classifier. Hidden links are not returned.
        '''
        edges = self.graph.edges
        return [idx for idx in self.idxEdges if edges[idx].rating >= likeThr and not(edges[idx].hidden)]

    def get_ratings(self)->dict:
        '''movie ratings
        '''
        edges = self.graph.edges
        return [(edges[idx].movieId, edges[idx].rating) for idx in self.idxEdges]

    def get_timeRtg(self):
        edges = self.graph.edges
        return [(edges[idx].movieId, edges[idx].timeRtg) for idx in self.idxEdges]

    def get_tags(self):
        edges = self.graph.edges
        return [(edges[idx].movieId, edges[idx].tags) for idx in self.idxEdges]

    def get_timeTags(self):
        edges = self.graph.edges
        return [(edges[idx].movieId, edges[idx].timeTags) for idx in self.idxEdges]

    def get_labels(self)->list:
        '''movies that the user likes. These are the labels of the user if you think
        of a recommendation system as a classifier. It is controled by the HP likeThr.
        '''
        edges = self.graph.edges
        idxLabels = self._get_idxLabels()
        return [edges[idx].movieId for idx in idxLabels]

    def get_nLabels(self)->int:
        '''number of labels
        '''
        return len(self.get_labels())

    def get_hidden(self)->list:
        '''hidden edges
        '''
        edges = self.graph.edges
        idxEdges = self.idxEdges
        return [(edges[idx].movieId, edges[idx].hidden) for idx in idxEdges if edges[idx].hidden]

    def get_nHidden(self)->int:
        '''number of hidden edges
        '''
        return len(self.get_hidden())

    def get_pHidden(self)->float:
        '''proportion of hidden edges
        '''
        if self.get_degree() !=0:
            return self.get_nHidden() / self.get_degree()
        else:
            return np.nan

    def get_features(self, fncts):
        '''returns user node features
        '''
        # -- Getting User Data
        ratings = self.get_ratings()
        tags = self.get_tags()
        timeRtg = self.get_timeRtg()
        timeTags = self.get_timeTags()

        return np.array([fncts[k](ratings, tags, timeRtg, timeTags) for k in range(len(fncts))])
    pass

class MovieNode(_Node):
    def __init__(self, nodeId: int):
        super().__init__(nodeId)
        pass

    def get_ratings(self):
        edges = self.graph.edges
        return [(edges[idx].userId, edges[idx].rating) for idx in self.idxEdges]

    def get_timeRtg(self):
        edges = self.graph.edges
        return [(edges[idx].userId, edges[idx].timeRtg) for idx in self.idxEdges]

    def get_tags(self):
        edges = self.graph.edges
        return [(edges[idx].userId, edges[idx].tags) for idx in self.idxEdges]

    def get_timeTags(self):
        edges = self.graph.edges
        return [(edges[idx].userId, edges[idx].timeTags) for idx in self.idxEdges]

    def get_genre(self):
        '''Not implemented for now
        '''
        return None

    def get_imdb(self):
        '''Not implemented for now
        '''
        return None

    def get_features(self, fncts: list):
        '''returns movie node features
        BEING IMPLEMENTED
        '''
        # -- Gathering User Opinion
        ratings = self.get_ratings()
        tags = self.get_tags()
        timeRtg = self.get_timeRtg()
        timeTags = self.get_timeTags()

        # -- Getting Movie Data
        genre = self.get_genre()
        imdb = self.get_imdb()

        return np.array([fncts[k](ratings, tags, timeRtg, timeTags, genre, imdb) for k in range(len(fncts))])



    pass
