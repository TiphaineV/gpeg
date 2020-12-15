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
    alpha = 0.7 # test proportion in the split

    # -- Graph construction + train_test_split
    graph = FastGraph()
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
