'''
Trivial Recommender System
'''

#%% Modules
# standard
import numpy as np

# personal
from _recSystems import _Clf
from node import UserNode, MovieNode
from fastGraph import FastGraph
from context import userData

#%% Trivial Recommendation System
class TrivialClf(_Clf):
    def __init__(self):
        super().__init__()
        pass

    def fit(self, edges):
        movieNodes = FastGraph.group_by_movie(edges)
        self.idPred = max(movieNodes, key= lambda x : movieNodes[x].get_avgRating())
        pass


    def predict(self, edges):
        ''' based on the average movie rating
        '''
        pred = []

        try:
            idPred = self.idPred
        except AttributeError:
            raise Exception('fit method has not been called')

        for edge in edges:
            pred.append(edge.movieId == idPred)

        return np.array(pred).astype('uint8')

if __name__ =='__main__':
    pass
