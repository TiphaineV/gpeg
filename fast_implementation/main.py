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


def main():
    # -- Graph construction + train_test_split
    graph = FastGraph()
    trainEdges, testEdges = graph.train_test_split(alpha = 0.2)

    # -- Classification Rec system + fit
    clf = TrivialClf()
    clf.fit(trainEdges)

    # -- Prediction
    testUsers = FastGraph.group_by_user(testEdges)
    pred = clf.predict(testUsers,nRec=3)
    print('Predictions: \n', pred)

    # -- Scoring
    score = clf.score(testUsers, nRec=3)
    print(score)

    pass

if __name__ == '__main__':
    main()
    pass
