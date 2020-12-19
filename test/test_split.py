'''Could not test this functionnality independantly from get_..._edges
'''
import unittest
import numpy as np
import numpy.random as rd
from contextTest import FastGraph,Edge


class TestSplit(unittest.TestCase):
    def setUp(self):
        '''sets the graph with hand made edges
        '''
        # -- building the graph
        graph = FastGraph()
        params = [(uId, mId, rd.choice([k*0.5 for k in range(11)]), []) 
                                    for uId in range(1,11)
                                    for mId in range(1,101)]

        edges = np.array([Edge(*tpl) for tpl in params])
        graph.edges = edges

        # -- making the split
        alpha = 0.25
        trainEdges, testEdges = graph.train_test_split(alpha)
        

        self.edges = edges
        self.alpha = alpha
        self.trainEdges = trainEdges
        self.testEdges = testEdges
        pass

    def test_proportion(self):
        '''teste si la proportion de lien de test est la bonne à 1e-2 près
        '''
        edges = self.edges
        trainEdges = self.trainEdges
        testEdges = self.testEdges

        ratio = np.round(len(testEdges)/ len(self.edges), decimals = 2)
        self.assertEqual(ratio, self.alpha)
        pass

    def test_partition(self):
        '''teste si on ne retrouve pas des liens d'entrainement parmi les liens de test et vice et versa
        '''
        testEdges = self.testEdges
        trainEdges = self.trainEdges

        tests = [ (edge in trainEdges) for edge in testEdges]

        self.assertFalse(any(tests))
        pass

if __name__ == '__main__':
    unittest.main()



