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
        '''Nothing parameter to fit for this clf
        '''
        self.xTrain, self.X_u, self.X_m = self._get_feature_matrix(edges)
        self.yTrain = self._get_labels(edges)
        pass

    def _get_known_edges(self, edges):
        ''' gets the edges for which we have data for both the user and the movie
        '''
        X_u = self.X_u
        X_m = self.X_m
        xTrain = self.xTrain
        d = np.column_stack((self.adj.row, self.adj.col))[edges]
        data = np.zeros((d.shape[0],), dtype=bool)

        # linear complexity -> bad
        for k in range(d.shape[0]):
            try:
                X_u.iloc[d[k][0]]
                X_m.iloc[d[k][1]]
                data[k] = True
            except IndexError:
                pass

        return data


    def predict(self, edges):
        ''' based on the average movie rating
        '''
        X_u = self.X_u
        X_m = self.X_m
        data = self._get_known_edges(edges)

        # -- Building the matrix
        index0 = np.where(data)[0]
        xTestKnown= pd.DataFrame(index = index0)
        
        V = X_u.iloc[self.adj.row[edges[data]]]
        V.index = index0
        W = X_m.iloc[self.adj.col[edges[data]]]
        W.index = index0
        
        xTestKnown[X_u.columns] = V
        xTestKnown[X_m.columns] = W

        # -- Make the prediction here
        yTestKnown = xTestKnown['xu0'] < xTestKnown['xm0']

        yTestUnknown = pd.Series(np.random.randint(2, size= len(np.where(np.logical_not(data))[0])), index= np.where(np.logical_not(data))[0])

        yPred = yTestKnown.append(yTestUnknown)

        print('random prop', len(yTestKnown)/len(yPred))
        return yPred

if __name__ =='__main__':
    pass
