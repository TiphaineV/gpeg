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
        '''Fits the recommender system to the input edges
        '''
        movieNodes = FastGraph.group_by_movie(edges)
        self.sortedMovies = sorted(movieNodes.values(), key= lambda x : x.get_avgRating())
        pass


    def predict(self, edges, nRec, nHidden= -1)->np.array,list:
        '''Recommends movies of the users whose Id is contained in the
        input edges.
        
        Parameters
        -------
            edges:
                the edges to predict

            nRec:
                the number of recommendations

            nHidden:
                shouldn't be changed. It has a use when scoring.
                
        Returns:
        --------
            predictions array (shape = nUsers, nRec) , userIds in edges
        '''
        # -- getting users
        users = FastGraph.group_by_user(edges, nHidden= nHidden)

        # -- prediction for one user (they're all the same)
        userPred = [ movie.nodeId for movie in self.sortedMovies[-nRec:]]
        
        # -- predictions for all users
        pred = [userPred for _ in range(len(users))]
        return np.stack(pred, axis = 0), list(users.keys())

if __name__ =='__main__':
    pass
