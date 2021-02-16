'''
Gradient Boosting
'''
from _recSystems import _Clf

import numpy as np
from sklearn.linear_model import LogisticRegression

class GradientBoostingClf(_Clf):
    def __init__(self, df, adj, likeThr=3.4, max_depth= None, max_features= None,
                 lr= 0.1, min_samples_split= 2, min_samples_leaf= 1, n_estimators=100,
                 subsample= 0.01, RANDOM_SEED=None):
        super().__init__(df,adj, likeThr, RANDOM_SEED)
        self.set_featFncts()

        # -- setting sklearn clf
        self.lr = lr
        self.subsample = subsample
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.max_features = max_features
        self.clf = GradientBoostingClassifier(n_estimators=self.n_estimators, 
                                              learning_rate=self.lr,
                                              subsample= self.subsample,
                                              max_depth=self.max_depth,
                                              max_features = self.max_features,
                                              min_samples_split= self.min_samples_split,
                                              min_samples_leaf= self.min_samples_leaf,
                                              random_state= self.RANDOM_SEED)
        pass

    def set_featFncts(self):
        # -- setting feature functions
        self.featFncts = {'user': [NodeFeatures.user_mean],
              'movie': [NodeFeatures.movie_mean]
              }
        pass