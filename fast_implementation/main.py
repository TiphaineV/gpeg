'''
What should look like training + testing
'''
# standard 
import numpy as np
import time

# personal
from _recSystems import _Clf
from node import UserNode, MovieNode
from fastGraph import FastGraph
from trivialClf import TrivialClf
from scorer import ClfScorer



def main():
    # -- Parameters
    alpha = 0.7 # test proportion in the split
    t0 = time.time()

    # -- Graph construction + train_test_split
    graph = FastGraph()
    print('Graph Construction:', time.time() - t0)
    trainEdges, testEdges = graph.train_test_split(alpha= alpha)

    # -- Fitting recommender system
    clf = TrivialClf()
    clf.fit(trainEdges)

    # -- Scoring
    scorer = ClfScorer()
    score = scorer.score(clf, testEdges)

    pass

if __name__ == '__main__':
    main()
    pass
