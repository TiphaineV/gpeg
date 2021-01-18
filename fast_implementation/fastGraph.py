'''
Builds the graph, quickly
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
    def __init__(self, userData = None, nChunk= 5, path= None):
        '''
        Parameters
        --------
        size: str
            'small' (100K), 'heavy' (20M)
        '''
        # -- IO
        print('Graph init ...')
        if path != None:
            self.load_adjency(path)
        # -- Attributes
        if userData !=None and path == None:
            self.set_adjency(userData, nChunk= nChunk)

        self.rowFormat = sparse.csr_matrix(self.adjency)
        self.colFormat = sparse.csc_matrix(self.adjency)
        pass

    def get_user(self, userId: int):
        return self.rowFormat[userId]

    def get_movie(self, movieId: int):
        return self.colFormat[:,movieId]

    def load_adjency(self, path):
        try:
            self.adjency = sparse.load_npz(path)
            self.edges = self.adjency.data

        except FileNotFoundError:
            print("file was not found, please try again or provide userData")
            raise
        pass

    def save_adjency(self, fileName):
        sparse.save_npz(fileName, self.adjency)
        pass


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