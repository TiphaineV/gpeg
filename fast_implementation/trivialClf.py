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

#%% Trivial Recommendation System
class TrivialClf(_Clf):
    def __init__(self):
        super().__init__()
        pass

    def set_featFncts(self):
        # -- feature function definition
        def average_rating(ratings, tags, timeRtg, timeTags):
            return sum(tpl[1] for tpl in ratings) / len(ratings)

        # -- setting feature functions
        self.featFncts = {'user': [average_rating],
                          'edge': [],
                          'movie': []
                        }
        pass

    def fit(self, edges):
        '''Nothing to fit for this clf
        '''
        xTrain = self._get_feature_matrix(edges)
        pass


    def predict(self, edges):
        ''' based on the average movie rating
        '''
        xTest = self._get_feature_matrix(edges)
        return (xTest > 3.2).astype('uint8')

if __name__ =='__main__':
    pass
