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
        ''' fits the model'''

        movieNodes = FastGraph.group_by_movie(edges)
        self.sortedMovies = sorted(movieNodes.values(), key= lambda x : x.get_avgRating())
        pass


    def predict(self, userIds: np.array, nRec=1):
        '''Predicts links for the users given.
        Parameters
        -------
            userArr: list or dictionnary

        Returns
        -------
            recommended movies.
        '''
        userPred = [ movie.nodeId for movie in self.sortedMovies[-nRec:]]
        pred = [userPred for _ in range(len(userIds))]
        return np.stack(pred, axis = 0)

if __name__ =='__main__':
    pass