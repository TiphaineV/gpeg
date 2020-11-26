'''
Splits data into training and validation data
'''
#%% Modules
#standard
import numpy.random as rd
import time

#personal
from graph import Graph

#%% Split class
class Split:
    def __init__(self,graph: Graph):
        self.graph = graph
        pass

    def get_train_test_split(self, alpha, length = False):
        '''splits data at random into a training set and a test set.

        Parameters
        -------
            alpha : float in [0,1]
            test size, alpha = | test data | / | all data | 

            length : bool
            whether or not it should return the length
            of both

        Returns
        -------
            if not(length):
                (genTrain, genTest) : generators
                edges of the train set and edges of the test set

            if length:
                (genTrain, genTest, nTrain, nTest)
        
        '''
        graph = self.graph
        if alpha >= 1 or alpha <=0 or not(isinstance(alpha,float)):
            raise ValueError('alpha must be a float in ]0,1[')

        nbEdges = graph.get_nbEdges()
        nTest = int(alpha*nbEdges)
        indexes = [ k for k in range(nbEdges) ] 
        rd.shuffle(indexes)
        idxsTrain, idxsTest = iter(sorted(indexes[nTest:])), iter(sorted(indexes[:nTest]))
        del indexes

        def indexes_gen(graph, idxs):
            genEdges = graph.get_genEdges()
            idx = next(idxs)
            for idxEdge, edge in enumerate(genEdges):
                if idxEdge == idx:
                    yield edge
                    try:
                        idx = next(idxs)
                    except StopIteration:
                        print('empty indexes gen')
                        print('idx', idx)
                        break
        if not(length):
            return indexes_gen(graph,idxsTrain), indexes_gen(graph,idxsTest)
        else:
            return indexes_gen(graph,idxsTrain), indexes_gen(graph,idxsTest), nbEdges - nTest, nTest


#%% main
if __name__ == '__main__':
    def test_nb():
        graph = Graph()
        genTrain, genTest = Split(graph).get_train_test_split(0.2)
        print('nbEdges ', graph.get_nbEdges())
        print('Train Edges')
        t0 = time.time()
        k = 0
        for edge in genTrain:
            k += 1
            pass
        print('nb of train edges ', k)
        print('Done ({}.s)'.format(time.time() - t0))

        print('Test Edges')
        t0 = time.time()
        k = 0
        for edge in genTest:
            k += 1
            pass
        print('nb of test edges ', k)
        print('Done ({}.s)'.format(time.time() - t0))
        pass

    def test_data():
        graph = Graph()
        genTrain, genTest = Split(graph).get_train_test_split(0.2)
        print('nbEdges ', graph.get_nbEdges())
        print('Train Edges')
        k = 0
        for edge in genTest:
            print(edge)
            k+=1
            if k ==7:
                break
        pass
    test_data()











