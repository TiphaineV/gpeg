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
    def __init__(self, df, adj):
        super().__init__(df)
        self.adj = adj
        pass

    def set_featFncts(self):
        # -- feature function definition
        def user_mean(dfByUser:pd.DataFrame):
            return dfByUser['rating'].agg(np.mean)

        def user_corr(dfByUser:pd.DataFrame):
            #-- not working yet
            return dfByUser[['rating', 'movieId']].apply(corr_custom)

        def movie_mean(dfByMovie:pd.DataFrame):
            return dfByMovie['rating'].agg(np.mean)

        # -- setting feature functions
        self.featFncts = {'user': [user_mean],
              'movie': [movie_mean]
              }
        pass

    def fit(self, edges):
        '''Nothing to fit for this clf
        '''
        self.xTrain, self.X_u, self.X_m = self._get_feature_matrix(edges)
        self.yTrain = self._get_labels(edges)
        pass

    def _get_known_edges(self, edges):
        ''' gets the edges for which we have data for both the user and the movie
        '''
        X_u = self.X_u
        X_m = self.X_m
        xTrain =self.xTrain
        d = np.column_stack((self.adj.row, self.adj.col))[edges]
        # -- Getting edges for which users and movies have been seen during training
        uniqueU, idxU = np.unique(self.adj.row[edges], return_indices=True)
        uniqueM, idxU = np.unique(self.adj.col[edges], return_indices=True)
        _,_, commU = np.intersect1d(X_u['userId'], uniqueU, assume_unique= True, return_indices= True)
        _,_, commM = np.intersect1d(X_m['movieId'], uniqueM, assume_unique= True, return_indices= True)

        knownU = np.concatenate([idxU[commU[k]: commU[k]+1] if k < len(commU) -1 else [idxU[commU[k]:]]] for k in range(len(commU)))
        knownM = np.concatenate([idxU[commM[k]: commM[k]+1] if k < len(commM) -1 else [idxM[commM[k]:]]] for k in range(len(commM)))
        knownE = edges[np.intesect1d(knownU, knownM, assume_unique= False)]

        # -- Getting the others
        unknownE = np.setdiff1d((edges, knownE), assume_unique=True)

        return knownE, unknownE


    def predict(self, edges):
        ''' based on the average movie rating
        '''
        knownE, unknownE = self._get_known_edges(edges)

        # -- Building the matrix
        xTestKnown= pd.DataFrame(index = knownE)
        xTestKnown[X_u.columns] = X_u.iloc[self.adj.row[knownE]]
        xTestKnown[X_m.columns] = X_m.iloc[self.adj.col[knownE]]

        yTestKnown = xTestKnown['xu0'] < xTestKnown['xm0']

        yTestUnknown = pd.DataFrame(np.random.randint(2, size= len(unknownE)), index= unknownE)

        yTestKnown.append(yTestKnown, sort=True)

        return yTestKnown

if __name__ =='__main__':
    pass
