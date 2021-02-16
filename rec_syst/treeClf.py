'''
Tree
'''

#%% Modules
from _recSystems import _Clf

import numpy as np
from sklearn.tree import DecisionTreeClassifier




#%% Trivial Recommendation System
class TreeClf(_Clf):
    def __init__(self, df, adj, likeThr=3.4, max_depth= None, min_samples_split= 2, min_samples_leaf= 1, 
                 RANDOM_SEED=None):
        super().__init__(df,adj, likeThr, RANDOM_SEED)
        self.set_featFncts()

        # -- setting sklearn clf
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.clf = DecisionTreeClassifier(max_depth=self.max_depth,
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
