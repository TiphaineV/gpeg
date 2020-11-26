'''
Trivial Recommender System
'''

#%% Modules
# standard
import numpy as np
from scipy import sparse
from scipy.sparse import csr_matrix, lil_matrix
from types import GeneratorType

# personal
from _recSystems import _PredRecSystem
from node import UserNode, MovieNode
from graph import Graph
from split import Split
from context import ratings, movies, tags

#%% Trivial Recommandation System
class RecSystemTrivial(_PredRecSystem):
    def __init__(self, graph: Graph):
        super().__init__(graph)
        pass

    def predict_user(self, userId : int)->int:
        '''recommend best rated movie in the DB
        '''
        graph = self.graph
        movieNodes = graph.movieNodes
        return max(movieNodes, key = MovieNode.get_avgRating).nodeId

    def predict(self, userArr: np.array)->csr_matrix:
        '''Predicts links from a list of user ids.

        Returns
        -------
            recommended movies. Each line corresponds to
            a user prediction, one hot encoded.


        '''
        pred = [self.predict_user(userArr[0])] * len(userArr)

        # TO DO : add to rec sys
        n = len(pred)
        data = tuple(1 for _ in range(n))
        indices = tuple(idx for idx in pred )
        indptr = tuple(k for k in range(n+1))
        return csr_matrix((data,indices,indptr),
                shape = (len(userArr), len(self.graph.movieNodes)))

    def predict_from_gen(self, gen: GeneratorType, genLength: int)->lil_matrix:
        '''Predicts links from a data generator

        Parameters
        -------
            gen: edges generator
            yields userId data. For the moment it should be of
            type (userId, movieId, movieRating).
            It could change in the future.

            genLength:
            useful for the implementation

        Returns
        -------
            recommended movies. Each line corresponds to
            a user prediction, one hot encoded.
        
        '''
        # -- Constructing sparse matrix incrementally
        y = lil_matrix((genLength, len(self.graph.movieNodes)), dtype= np.double)
        indices = ( self.predict_user(userId) for userId,_,_ in gen )
        
        for idx,pred in enumerate(indices):
            y[idx,pred] = 1

        return y


if __name__ == '__main__':
    #-- Training 

    # -- Testing
    def test_pred():
        graph = Graph()
        mvPred = RecSystemTrivial(graph).predict([2,3,4,5,6,7])
        print(mvPred[:5])
        pass

    def test_predict():
        graph = Graph()
        recSys = RecSystemTrivial(graph)
        genTrain, genTest = Split(graph).get_train_test_split(alpha= 0.2)
        userArr = []
        y = []
        for edge in genTest:
            userArr.append(edge[0])
            y.append(edge[1])
        userArr = np.array(userArr)

        yPred = recSys.predict(userArr)

        print('Prediction: ', yPred[:10])
        print('Ground Truth: ', y[:10])
        pass

    def test_predict_from_gen():
        graph = Graph()
        recSys = RecSystemTrivial(graph)
        split = Split(graph)
        genTrain, genTest, _, nTest = split.get_train_test_split(alpha= 0.2, length = True)
        yPred = recSys.predict_from_gen(genTest, nTest)
        print('prediction: ', yPred[:10])
        pass

    test_predict_from_gen()
