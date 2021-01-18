'''
Trivial Recommender System
'''

#%% Modules
# standard
import numpy as np

# personal
from _recSystems import _Clf
from fastGraph import Graph
from features import NodeFeatures
import pandas as pd

#%% Trivial Recommendation System
class TrivialClf(_Clf):
    def __init__(self, df, adj):
        super().__init__(df)
        self.adj = adj
        pass

    def set_featFncts(self):
        # -- feature function definition
        # def user_mean(dfByUser:pd.DataFrame):
            # return dfByUser['rating'].agg(np.mean)

        # def user_corr(dfByUser:pd.DataFrame):
            # #-- not working yet
            # return dfByUser[['rating', 'movieId']].apply(corr_custom)

        # def movie_mean(dfByMovie:pd.DataFrame):
            # return dfByMovie['rating'].agg(np.mean)

        # -- setting feature functions
        self.featFncts = {'user': [NodeFeatures.user_mean],
              'movie': [NodeFeatures.movie_mean]
              }
        pass

    def fit(self, edges):
        '''Nothing parameter to fit for this clf
        '''
        self.xTrain, self.X_u, self.X_m = self._get_feature_matrix(edges)
        pass

    def _predict_known(xTestKnown):
        return xTestKnown['xu0'] < xTestKnown['xm0']

if __name__ =='__main__':
    pass
