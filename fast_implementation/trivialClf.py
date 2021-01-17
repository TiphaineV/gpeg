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
    def __init__(self, df):
        super().__init__(df)
        pass

    def set_featFncts(self):
        # -- feature function definition

        def edge_has_tag(df:pd.DataFrame):
            return 1- df['tag'].isna().astype('uint8')

        def edge_timestamps(df:pd.DataFrame):
            return (df['timestamp_rating'] < df['timestamp_tag']).astype('uint8')

        def user_mean(dfByUser:pd.DataFrame):
            return dfByUser['rating'].agg(np.mean)

        def user_corr(dfByUser:pd.DataFrame):
            #-- not working yet
            return dfByUser[['rating', 'movieId']].apply(corr_custom)

        def movie_mean(dfByMovie:pd.DataFrame):
            return dfByMovie['rating'].agg(np.mean)

        # -- setting feature functions
        self.featFncts = {'user': [user_mean],
              'edge': [edge_has_tag, edge_timestamps],
              'movie': [movie_mean]
              }
        pass

    def fit(self, edges):
        '''Nothing to fit for this clf
        '''
        xTrain = self._get_feature_matrix(edges)
        yTrain = self._get_labels(edges)
        pass


    def predict(self, edges):
        ''' based on the average movie rating
        '''
        xTest = self._get_feature_matrix(edges)
        return xTest['xu0'] < xTest['xm0']

if __name__ =='__main__':
    pass
