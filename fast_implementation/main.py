'''
What should look like training + testing
'''
# standard 
import numpy as np

# personal
from _recSystems import _Clf
from node import UserNode, MovieNode
from fastGraph import FastGraph
from context import userData
from trivialClf import TrivialClf
from scorer import ClfScorer


def main():
    # -- Parameters
    nRec = 7 # number of recommendation the recommender system should make
    alpha = 0.7 # test proportion in the split
    nLabels = 5
    degreeEx = 2

    # -- Graph construction + train_test_split
    graph = FastGraph()
    trainEdges, testEdges = graph.train_test_split(alpha= alpha)


    # -- Fitting recommender system
    clf = TrivialClf()
    clf.fit(trainEdges)

    # -- Scoring
    scorer = ClfScorer(graph)
    score = scorer.score(clf, testEdges, nRec, nLabels, degreeEx= degreeEx)
    print(score)

    pass

if __name__ == '__main__':
    main()
    pass
