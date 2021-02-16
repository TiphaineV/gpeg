'''
Recommender systems abstract classes.
'''
#%% Modules
#standard
from abc import ABC, abstractmethod
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd

#%% Trivial Recommandation System
class _RecSystem(ABC):
    '''
    Abstract class for recommender systems.
    '''
    def __init__(self):
        pass

    @abstractmethod
    def fit(self, edges):
        pass

    @abstractmethod
    def predict(self, edges, *args):
        pass
    pass



class _Clf(_RecSystem):
    '''
    Classifier recommendation system
    '''
    def __init__(self, df, adj, likeThr, RANDOM_SEED= None):
        super().__init__()
        self.df = df
        self.adj = adj
        self.likeThr = likeThr
        self.scaler = None
        self.RANDOM_SEED = None
        pass
    
    def reset(self):
        self.scaler= None
        self.xTrain= None
        self.X_u = None
        self.X_m = None
        self.yTrain = None

    def _get_feature_matrix(self, edges):
        df = self.df.iloc[edges]
        featFncts = self.featFncts

        dfByUser = df.groupby('userId')
        dfByMovie = df.groupby('movieId')

        X = pd.DataFrame() 
        X['userId'] = df['userId']
        X['movieId'] = df['movieId']
        X_u = pd.DataFrame(index= df['userId'].drop_duplicates().sort_values())
        X_m = pd.DataFrame(index= df['movieId'].drop_duplicates().sort_values())

        k = 0
        for featFnct in featFncts['user']:
            dfU= featFnct(dfByUser)
            if isinstance(dfU, pd.Series):
              X_u['xu'+str(k)] = dfU
              k+=1
            
            if isinstance(dfU, pd.DataFrame):
              # comes from ohe
              colU = X_u.columns
              for col in colU:
                X_u['xu'+str(k)] = dfU[col]
                k += 1
        k = 0
        for featFnct in featFncts['movie']:
            dfM= featFnct(dfByMovie)
            if isinstance(dfM, pd.Series):
              X_m['xm'+str(k)] = dfM
              k+=1
            
            if isinstance(dfM, pd.DataFrame):
              # comes from ohe
              colM = dfM.columns
              for col in colM:
                X_m['xm'+str(k)] = dfM[col]
                k += 1
        
        xTrain = X.merge(X_u, on='userId', how='left').merge(X_m, on='movieId', how='left')
        xTrain.index = df.index
        return xTrain, X_u, X_m

    def _get_labels(self, edges):
        return (self.df['rating'].iloc[edges] > self.likeThr).astype('uint8')

    def _get_known_edges(self, edges):
        ''' gets the edges for which we have data for both the user and the movie
        '''
        X_u = self.X_u
        X_m = self.X_m
        xTrain = self.xTrain
        d = np.column_stack((self.adj.row, self.adj.col))[edges]
        data = np.zeros((d.shape[0],), dtype=bool)

        unicU, invU  = np.unique(self.adj.row[edges], return_inverse=True)
        _, _, commU = np.intersect1d(self.xTrain['userId'], unicU, assume_unique=False, return_indices=True)
        maskU = np.zeros_like(unicU, dtype= bool)
        maskU[commU] = True
        knownEdgeUser = np.where(maskU[invU])

        unicM, invM  = np.unique(self.adj.col[edges], return_inverse=True)
        _, _, commM = np.intersect1d(self.xTrain['movieId'], unicM, assume_unique=False, return_indices=True)
        maskM = np.zeros_like(unicM, dtype= bool)
        maskM[commM] = True
        knownEdgeMovie = np.where(maskM[invM])
        
        # index in xTrain
        knownE = edges[np.intersect1d(knownEdgeUser, knownEdgeMovie, assume_unique=True)]

        knownU = self.adj.row[knownE]
        knownM = self.adj.col[knownE]

        # -- getting data on user
        unicU = np.unique(knownU)
        _,commX_u, _ = np.intersect1d(X_u.index, unicU, assume_unique=True, return_indices=True)
        X_uT = X_u.iloc[commX_u] 

        # -- getting data on movies
        unicM = np.unique(knownM)
        _,commX_m, _ = np.intersect1d(X_m.index, unicM, assume_unique=True, return_indices=True)
        X_mT = X_m.iloc[commX_m]

        # -- Building the matrix
        X = pd.DataFrame({'userId': knownU, 'movieId': knownM})
        xTestKnown = X.merge(X_uT, on='userId', how='left').merge(X_mT, on='movieId', how='left')
        xTestKnown.index = knownE
        unknownE = np.setdiff1d(edges, knownE, assume_unique=True)
        yTestUnknown = pd.Series(np.random.randint(2, size= len(unknownE)), index= unknownE)

        return xTestKnown, yTestUnknown
    
    def _set_scaler(self, X):
        scaler = StandardScaler()
        scaler.fit(X)
        self.scaler = scaler
        pass

    def _preprocess(self, X):
        '''scaling applied to both xTrain and xTest.
        '''
        nonBoolCols = X.columns.difference(X.columns[X.dtypes.values == 'bool']).drop(['userId','movieId'])
        if self.scaler is None:
          self._set_scaler(X[nonBoolCols])
        assert X[nonBoolCols].iloc[:,0].mean() > 1e-13
        mean_ = self.scaler.mean_
        scale_ = self.scaler.scale_
        X[nonBoolCols] -= mean_
        try:
          X[nonBoolCols] *= 1/ (scale_ + 1e-2)
        except ZeroDivisionError:
          print('Constant columns in the DS')
          raise
        return X.drop(columns= ['userId', 'movieId'])
    
    def _get_sparse(self, X, dType):
        '''get preprocessed data as a sparse matrix for the classifier
        '''
        if dType == 'csr':
          return X.astype(pd.SparseDtype('float32', 0.)).sparse.to_coo().tocsc()
        elif dType == 'csc':
          return X.astype(pd.SparseDtype('float32', 0.)).sparse.to_coo().tocsc()
        elif dType == 'coo':
          return X.astype(pd.SparseDtype('float32', 0.)).sparse.to_coo()
        elif dType == None:
          print('Warning: Dense matrix provided to classifier')
          return X
        else:
          raise ValueError('Provide a sparse matrix type or None')
    
    def fit(self, edges, dType='csr'):
        self.xTrain, self.X_u, self.X_m = self._get_feature_matrix(edges)
        self.yTrain = self._get_labels(edges)
        self.clf.fit(self._get_sparse(self._preprocess(self.xTrain), dType= dType), self.yTrain)
        pass

    def _predict_known(self, xTestKnown, dType):
        return pd.Series(self.clf.predict(self._get_sparse(self._preprocess(xTestKnown), dType)),
                                          index= xTestKnown.index)


    def predict(self, edges, dType='csr'):
        xTestKnown, yTestUnknown = self._get_known_edges(edges)

        # -- prediction
        yTestKnown = self._predict_known(xTestKnown, dType)

        # -- check if it is a partition
        assert len(set(yTestKnown.index).intersection(yTestUnknown.index)) ==0
        assert len(set(yTestKnown.index).union(yTestUnknown.index)) == len(edges)
        yPred = pd.Series(np.zeros_like(edges, dtype='uint8'), index=edges)
        yPred[yTestKnown.index] = yTestKnown.astype('uint8')
        yPred[yTestUnknown.index] = yTestUnknown.astype('uint8')
        return yPred
    pass