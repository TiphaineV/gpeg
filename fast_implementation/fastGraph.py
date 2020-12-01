'''
Makes the graph, quickly
'''

#%% Modules
#standard
from abc import ABC, abstractmethod
import time
#personal
from edge import Edge
from context import userData
from node import MovieNode, UserNode
from split import train_test_split
import numpy.random as rd


#%% FastGraph class
class _Graph(ABC):
    def __init__(self):
        # -- Attributes
        self.edges = []
        movieIds = set()
        userIds = set()

        # -- Adding ref to the graph 
        MovieNode.set_graph(self)
        UserNode.set_graph(self)
        pass

    @abstractmethod
    def set_edges(self):
        '''Should also set movieIds and userIds
        '''
        pass

    @classmethod
    def group_by_user(cls, edges, degreeMin= 1):
        '''
        can be called by other classes, if not fast change the structure
        '''
        # -- getting all user nodes
        userNodes = {}
        for idx, edge in enumerate(edges):
            userId = edge.userId
            try:
                userNodes[userId].add(idx)
            except KeyError:
                node = UserNode(userId)
                userNodes.update({userId : node})

        # -- keeping only those with degree > degreeMin
        ids = userNodes.keys()
        return {idd : userNodes[idd] for idd in ids
                                     if userNodes[idd].get_degree() >= degreeMin}

    @classmethod
    def group_by_movie(cls, edges, degreeMin= 1):
        '''
        can be called by other classes, could be faster
        '''
        movieNodes = {}
        for idx, edge in enumerate(edges):
            movieId = edge.movieId
            try:
                movieNodes[movieId].add(idx)
            except KeyError:
                node = MovieNode(movieId)
                movieNodes.update({movieId : node})

        # -- keeping only those with degree > degreeMin
        ids = movieNodes.keys()
        return {idd : movieNodes[idd] for idd in ids 
                                      if movieNodes[idd].get_degree() >= degreeMin}
    
    def get_edges(self, group = 'all'):
        if group == 'all':
            return self.edges
        else:
            edges = self.edges
            return [edge for edge in edges if edge.group == group]

    def get_movieNodes(self, degreeMin= 1, group= 'all'):
        edges = self.get_edges(group)
        return group_by_movie(edges, degreeMin)

    def get_userNodes(self, degreeMin= 1, group= 'all'):
        edges = self.get_edges(group)
        return group_by_user(edges, degreeMin)

    pass

class FastGraph(_Graph):
    def __init__(self):
        super().__init__()
        self.set_edges()

    def set_edges(self):
        edges = []
        movieIds = set()
        userIds = set()

        for idx in range(len(userData)):
            # -- keys : userId, movieId, rating, tags, timestamps...
            row = userData.iloc[idx]

            # -- getting ids, ratings, tags from DB
            userId, movieId= row['userId'], row['movieId']
            rating, tags = row['rating'], row['tag']

            # -- updating edge list, and keeping all id values
            edges.append(Edge(userId, movieId, rating, tags))
            movieIds.add(movieId)
            userIds.add(userId)

        # -- setting attributes
        self.edges = edges
        self.movieIds = movieIds
        self.userIds = userIds
        pass

    def train_test_split(self, alpha: float):
        '''
        '''
        # -- Checking parameter alpha
        if alpha >= 1 or alpha <=0 or not(isinstance(alpha,float)):
            raise ValueError('alpha must be a float in ]0,1[')

        # -- Parameters
        edges = self.edges
        n = len(edges)
        nTest = int(alpha * n)
        indexes = list(range(n))

        # -- Randomizing data
        rd.shuffle(indexes)

        # -- Getting the split
        idxTrain, idxTest = sorted(indexes[nTest:]), sorted(indexes[:nTest])
        nTrain, nTest = len(idxTrain), len(idxTest)

        # -- Fast implementation : a pointer follows each list.
        k = 0
        ptrTrain = 0
        ptrTest = 0
        while k < n:
            if ptrTrain < nTrain and idxTrain[ptrTrain] == k:
                edges[k].set_group('train')
                ptrTrain +=1
            elif ptrTest < nTest and idxTest[ptrTest] == k:
                edges[k].set_group('test')
                ptrTest += 1
            else:
                raise ValueError('2 pointers approach failed')
            k +=1

        self.edges = edges
        return self.get_edges(group= 'train'), self.get_edges(group= 'test')





if __name__ == '__main__':
    pass





