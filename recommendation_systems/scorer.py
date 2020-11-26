'''
Scorer classes.
Inspired by _scorers.py of sklearn.
'''
#%% Modules
#standard
import numpy as np
from abc import ABC,abstractmethod
from types import FunctionType
from scipy.sparse import csr_matrix

# personal
from _recSystems import _RecSystem
from graph import Graph
from recSystemTrivial import RecSystemTrivial
from split import Split

#%% Score functions
scoreFunctions = { 
    'mse' : lambda y,yPred :  (
                mat := y.dot(yPred.T), # assignement op.
                nRow := mat.shape[0],
                sum(mat[i,i] for i in range(nRow))/nRow
            )
    }

#%% Classes
class _Scorer(ABC):
    '''
    Abstract scorer class. 
    '''
    def __init__(self, scoreFunc: FunctionType):
        '''
        Parameters
        -------
            scoreFunc : function(ypred, y)
                function used to compare ground truth and predicted data

        NB: initializing it with score_func as attribute allows to
        compare score from different recSyst easily with the same metric.
        '''
        self.scoreFunc = scoreFunc
        pass

    @abstractmethod
    def score(self, recSyst : _RecSystem, X, y):
        '''
        Parameters
        -------
            X : array-like (nRow,)
                data to give to the recommender system

            y : array-like (nRow, nbMovies)
                ground truth data. Each line should contain
                a movie id one hot encoded. Sparse Matrices should
                be prefered to conventional arrays for memory reduction.

        Returns
        --------
            score: float between 0 and 1.
        '''
        pass

class PredictScorer(_Scorer):
    '''
    Scorer based solely on the movie recommended
    '''
    def __init__(self, scoreFunc):
        super().__init__(scoreFunc)
        pass

    def score(self, recSyst, X, y):
        yPred = recSyst.predict(X)
        return self.scoreFunc(yPred,y)

class ProbaScorer(_Scorer):
    '''
    Scorer based on the probability of each user to
    like the movies in the DB.
    '''
    def __init__(self, scoreFunc):
        super().__init__(scoreFunc)
        pass

    def score(self, recSyst, X, y):
        '''
        NB : might not fit in memory.
        score might need to be computed using batches.
        '''
        yPred = recSyst.predict_proba(X) #shape = (len(X), nbMovies)
        return self.scoreFunc(yPred,y)


if __name__ == '__main__':
    import pdb

    def test_predict_scorer():
        # -- making the split
        graph = Graph()
        recSys = RecSystemTrivial(graph)
        genTrain, genTest = Split(graph).get_train_test_split(alpha= 0.2)
        userArr = []
        y = []
        for edge in genTest:
            userArr.append(edge[0])
            y.append(edge[1])
        X = np.array(userArr)
        print('ok')

        # -- y.to_csr()
        n = len(y)
        data = tuple(1 for _ in range(n))
        indices = tuple(idx for idx in y )
        indptr = tuple(k for k in range(n+1))
        y = csr_matrix((data,indices,indptr), shape = (n, len(graph.movieNodes)))

        pdb.set_trace()
        print('ok2')
        # -- scoring
        scoreFunc = scoreFunctions['mse']
        scorer = PredictScorer(scoreFunc)
        print('ok3')
        score = scorer.score(recSys, X, y)
        print('ok4')
        print('score', score)
        pass

    test_predict_scorer()


    pass








