'''
Builds the graph, quickly

Implementation
---------
    The idea is to go through the data only once, and from each row to build an edge. 
    The graph stores all these edges, and is kept as a reference for all the nodes. 
    The nodes don't store the edges, but only keep references to it. 
    If you need the user nodes or the movie nodes, the graph ties the edges to the nodes and 
    returns it fastly when you call the appropriate method.
    Now, why it has been done this way, is because it makes it easy to split the graph (cf
    FastGraph.train_test_split) : you can chose to use only a subset of the edges to tie to the nodes.
'''
#%% Modules
#standard
from abc import ABC, abstractmethod
import time
import numpy as np
import numpy.random as rd

#personal
from edge import Edge
from node import MovieNode, UserNode
from context import userData
from tqdm import tqdm



#%% FastGraph class
class _Graph(ABC):
    def __init__(self):
        # -- IO
        print('Graph init ...')
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
    def group_by(cls, method, edges, degreeMin=1):
        '''ties the provided edges to the nodes
        '''
        user = method is Edge.get_userId
        # -- getting all nodes
        nodes = {}
        for idx, edge in enumerate(edges):
            idd = method(edge)

            # -- add the node to the dict if it doesn't exist
            try:
                nodes[idd].add(idx)
            except KeyError:
                if user:
                    node = UserNode(idd)
                else:
                    node = MovieNode(idd)
                node.add(idx)
                nodes.update({idd : node})

        # -- keeping only those within a certain range of degree
        ids = nodes.keys()
        return {idd : nodes[idd] for idd in ids
                                         if nodes[idd].get_degree() >= degreeMin
                                         }

    @classmethod
    def group_by_user(cls, edges, degreeMin= 1)->dict:
        '''ties the provided edges to the user Nodes
        '''
        method = Edge.get_userId
        return cls.group_by(method, edges, degreeMin)


    @classmethod
    def group_by_movie(cls, edges, degreeMin= 1)->dict:
        '''ties the provided edges to the movie Nodes
        '''
        method = Edge.get_movieId
        return cls.group_by(method, edges, degreeMin)

    def get_edges(self, group = 'all'):
        if group == 'all':
            return self.edges
        else:
            edges = self.edges
            return [edge for edge in edges if edge.group == group]
    pass

class FastGraph(_Graph):
    def __init__(self):
        super().__init__()
        self.set_edges()

    def set_edges(self):
        edges = []

        for k,chunk in enumerate(userData):
            print('Processing chunk {}.'.format(k))
            for idx in tqdm(range(len(chunk))):
                # -- keys : userId, movieId, rating, tags, timestamps...
                row = userData.iloc[idx]

                # -- getting ids, ratings, tags from DB
                userId, movieId= row['userId'], row['movieId']
                rating, tags = row['rating'], row['tag']
                timeRtg, timeTags = row['timestamp_rating'], row['timestamp_tag']

                # -- updating edge list, and keeping all id values
                edges.append(Edge(userId, movieId, rating, tags, timeRtg, timeTags))

        # -- setting attributes
        self.edges = edges

        # -- IO
        print('Done')
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

        return self.get_edges(group= 'train'), self.get_edges(group= 'test')





if __name__ == '__main__':
    pass









