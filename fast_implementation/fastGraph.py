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
from context import userData
from node import MovieNode, UserNode



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

    def hide_edges(self, indices:list)->list:
        '''hides edges of the graph whose index is in indices input
        '''
        hiddenEdges = []
        for idx in indices:
            self.edges[idx].hide()
            hiddenEdges.append(self.edges[idx])
        return hiddenEdges

    def unhide_edges(self):
        '''sets hidden attribute of the edges of the graph to false
        '''
        edges = self.edges
        for edge in edges:
            edge.hidden = False
        pass


    @classmethod
    def group_by_user(cls, edges, nLabelsMin=0, degreeMin= 1, nHidden= -1)->dict:
        '''ties the provided edges to the user Nodes
        can be called by other classes
        '''
        # -- getting all user nodes
        userNodes = {}
        for idx, edge in enumerate(edges):
            userId = edge.userId

            # -- add the node to the dict if it doesn't exist
            try:
                userNodes[userId].add(idx)
            except KeyError:
                node = UserNode(userId)
                node.add(idx)
                userNodes.update({userId : node})

        # -- keeping only those within a certain range of degree and nLabel
        #    sometimes (scoring), we also want the nodes with a certain amount of hidden edges. 
        ids = userNodes.keys()
        if nHidden == -1:
            return {idd : userNodes[idd] for idd in ids
                                             if userNodes[idd].get_degree() >= degreeMin
                                             if userNodes[idd].get_nLabels() >= nLabelsMin
                                             }
        else:
            return {idd : userNodes[idd] for idd in ids
                                             if userNodes[idd].get_degree() >= degreeMin
                                             if userNodes[idd].get_nLabels() >= nLabelsMin
                                             if userNodes[idd].get_hidden() == nHidden
                                             }

    @classmethod
    def group_by_movie(cls, edges, degreeMin= 1)->dict:
        '''ties the provided edges to the movie Nodes
        can be called by other classes. Similar to group_by_user
        '''
        movieNodes = {}
        for idx, edge in enumerate(edges):
            movieId = edge.movieId
            try:
                movieNodes[movieId].add(idx)
            except KeyError:
                node = MovieNode(movieId)
                node.add(idx)
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
        '''returns the movieNodes
        '''
        edges = self.get_edges(group)
        return group_by_movie(edges, degreeMin)

    def get_userNodes(self, nLabelMin=0, degreeMin= 1, group= 'all'):
        '''returns the userNodes
        '''
        edges = self.get_edges(group)
        return group_by_user(edges, nLabelMin, degreeMin)

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
        self.edges = np.array(edges)
        self.movieIds = movieIds
        self.userIds = userIds

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









