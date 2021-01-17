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
import scipy.sparse as sparse
import pandas as pd



#%% FastGraph class
class Graph:
    def __init__(self, userData: pd.DataFrame, nChunk= 5):
        '''
        Parameters
        --------
        size: str
            'small' (100K), 'heavy' (20M)
        '''
        # -- IO
        print('Graph init ...')
        # -- Attributes
        self.set_adjency(userData, nChunk= nChunk)

        ## - Not quite sure this is standard
        self.rowFormat = sparse.csr_matrix(self.adjency)
        self.colFormat = sparse.csc_matrix(self.adjency)
        pass

    def get_user(self, userId: int):
        return self.rowFormat[userId]

    def get_movie(self, movieId: int):
        return self.colFormat[:,movieId]

    def set_adjency(self, userData, nChunk= np.inf):
        ''''''
        # -- Builds the matrix
        chunksize = int(1e6)
        rows = []
        cols = []
        data = []
        for k,chunk in enumerate(userData):
            print('Processing chunk {}.'.format(k))
            for idx in range(len(chunk)):
                # -- keys : userId, movieId.
                row = chunk.iloc[idx]

                # -- getting ids
                userId, movieId= row['userId'], row['movieId']

                # -- updating rows, cols, data
                rows.append(userId)
                cols.append(movieId)
                data.append(k*chunksize+idx)

            #### temp ####
            if k == nChunk - 1:
                break
        
        print(len(data), len(rows), len(cols))
        print(max(rows), max(cols))

        adjency = sparse.coo_matrix((data, (rows, cols)), shape=(max(rows)+1, max(cols)+1))

        self.adjency = adjency
        self.edges = adjency.data
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

        return edges[idxTrain], edges[idxTest]

if __name__ == '__main__':
    pass