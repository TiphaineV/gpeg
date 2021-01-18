'''
Trivial Recommender System
'''

#%% Modules
# standard
import numpy as np

# personal
from _recSystems import _Clf
from fastGraph import Graph
import pandas as pd

#%% Trivial Recommendation System
class TrivialClf(_Clf):
    def __init__(self, df, adj, featFncts):
        super().__init__(df, adj, featFncts)
        pass

    def fit(self, edges):
        '''Nothing parameter to fit for this clf
        '''
        self.xTrain, self.X_u, self.X_m = self._get_feature_matrix(edges)
        pass

    def _predict_known(self, xTestKnown):
        return xTestKnown['xu0'] < xTestKnown['xm0']

if __name__ =='__main__':
    pass
