'''
Logistic Regression
'''
from _recSystems import _Clf

import numpy as np
from sklearn.linear_model import LogisticRegression

class LogRegClf(_Clf):
    def __init__(self, df, adj, likeThr=3.4, C0= 1e0, balanced= True, RANDOM_SEED=None):
        super().__init__(df,adj, likeThr, RANDOM_SEED)
        self.set_featFncts()
        self.C0 = C0
        self.class_weight = 'balanced' if balanced else None
        self.clf = LogisticRegression(C = self.C0, class_weight=self.class_weight,
                                      solver= 'saga', random_state= self.RANDOM_SEED)
        pass

    def set_featFncts(self):
        # -- setting feature functions
        self.featFncts = {'user': [NodeFeatures.user_mean],
              'movie': [NodeFeatures.movie_mean]
              }