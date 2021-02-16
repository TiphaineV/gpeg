'''
Trivial Recommender System
'''
import numpy as np

class TrivialClf(_Clf):
    def __init__(self, df, adj, likeThr):
        self.set_featFncts()
        super().__init__(df,adj, likeThr, RANDOM_SEED= None)
        pass

    def set_featFncts(self):
        # -- setting feature functions
        self.featFncts = {'user': [NodeFeatures.user_mean],
              'movie': [NodeFeatures.movie_mean]
              }

    def fit(self, edges):
        '''Nothing parameter to fit for this clf
        '''
        self.xTrain, self.X_u, self.X_m = self._get_feature_matrix(edges)
        pass

    def _predict_known(self, xTestKnown, dType):
        return likeThr < xTestKnown['xm0']