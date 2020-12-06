'''
Scorer classes.
Inspired by _scorers.py of sklearn.
'''
#%% Modules
#standard
import numpy as np
from abc import ABC,abstractmethod

# personal
from _recSystems import _RecSystem
from fastGraph import FastGraph

#%% Classes
class _Scorer(ABC):
    '''
    Abstract scorer class. 
    '''
    def __init__(self, graph):
        '''Scorer needs a ref to the graph, for some computations.
        '''
        self.graph = graph
        pass

    @abstractmethod
    def score(self, clf, edges):
        '''
        Parameters
        -------
            clf: _recSystems._Clf
                the recommender system seen as a classifier

            edges: list[Edge]
                the edges you want to score
        Returns
        -------
            score: float or tuple
        '''
        pass

class ClfScorer(_Scorer):
    '''
    Scorer based solely on the movie recommended
    '''
    def __init__(self, graph):
        super().__init__(graph)
        pass

    def _get_labels(self, edges, nLabels, degreeEx = 1):
        '''get the labels of the users of the subgraph formed by the input edges.

        Parameters
        ------
            nLabel: int
                the number of labels you want to extract from the userNodes.
                Extracted edges will not be taken into account in the prediction,
                and will be seen as hidden.

            degreeEx : int
                the minimum degree the userNodes should keep after the extraction.

        Returns
        -------
            array of shape (n_user, nLabels), user keys
                user keys will be compared to the ones from the recommendation
        '''
        nLabelsMin = nLabels + degreeEx
        userNodes = FastGraph.group_by_user(edges, nLabelsMin= nLabelsMin)
        labels = []
        for userId in userNodes:
            userNode = userNodes[userId]
            hiddenEdges = userNode.hide_labels(nHide= nLabels)
            userLabels = [hiddenEdges[k].movieId for k in range(len(hiddenEdges))]
            labels.append(userLabels)
        return np.stack(labels, axis= 0), list(userNodes.keys())


    def score(self, clf, edges, nRec: int, nLabels: int, degreeEx= 1)-> tuple:
        '''scores the recommendation made for the users whose id is in the edge list

        Parameters
        -------
            clf: _recSystems._Clf
                the recommender system seen as a classifier

            edges: list[Edge]
                the edges you want to score

            nRec: int
                number of recommendations the classifier should make for each user. 

            nLabels: int
                number of labels to extract from the user nodes created with these edges

            degreeEx: int
                the minimum degree of the nodes after extraction

        Returns
        -------
            score : tuple
                precision, recall, f1-score

        '''
        # -- getting user labels
        yTrue, lKeys = self._get_labels(edges, nLabels, degreeEx)


        # -- user nodes will now have a minimum degree of degreeEx
        yPred, pKeys= clf.predict(edges, nRec, nHidden= nLabels) # dim nUsers, nRec
        
        # -- Unhide all edges, to avoid side effects on the graph
        self.graph.unhide_edges()
        
        if lKeys != pKeys:
            raise IndexError('the predictions order does not match the labels one')

        # -- computing metrics
        countTP = 0 # true positive count
        for nRow, true in enumerate(yTrue):
            pred = yPred[nRow]
            countTP += len(set(true).intersection(set(pred)))

        # -- precision, recall, f1-score
        precision = countTP / (nLabels**2) # TP / (TP + FN)
        recall = countTP / (nRec**2) # TP / (TP + FP)
        try:
            f1score = 2 * recall * precision / (recall + precision)
        except ZeroDivisionError:
            f1score = 0
        return precision, recall, f1score


class RatingScorer(_Scorer):
    '''
    Scorer based on the probability of each user to
    like the movies in the DB.
    '''
    def __init__(self, graph):
        super().__init__(graph)
        pass

    def score(self, recSyst, X, y):
        pass

if __name__ == '__main__':
    pass








