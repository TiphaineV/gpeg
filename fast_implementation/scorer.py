'''
Scorer classes.
Inspired by _scorers.py of sklearn.
'''
#%% Modules
#standard
import numpy as np
from abc import ABC,abstractmethod
from sklearn.metrics import classification_report, precision_score, recall_score, f1_score

# personal
from _recSystems import _RecSystem
from fastGraph import FastGraph
from context import likeThr


#%% Classes
class _Scorer(ABC):
    '''
    Abstract scorer class. 
    '''
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
    def score(self, clf, edges, metric= 'precision'):
        '''scores the recommendation made for the users whose id is in the edge list
        Available metrics are precision, recall and f1-score

        Parameters
        -------
            clf: _recSystems._Clf
                the recommender system seen as a classifier

            edges: list[Edge]
                the edges you want to score

        Returns
        -------
            score : tuple
                precision, recall, f1-score
        '''
        yPred = clf.predict(edges)
        yTrue = np.array([edge.rating > likeThr for edge in edges]).astype('uint8')
        print(np.sum(yPred))
        print(np.sum(yTrue))
        print(classification_report(yTrue, yPred, target_names = ['class 0', 'class 1']))

        if metric == 'precision':
            return precision_score(yTrue, yPred)
        elif metric == 'recall':
            return recall_score(yTrue, yPred)
        elif metric == 'f1-score':
            return f1_score(yTrue, yPred)
        else:
            raise ValueError('not supported metric, available are precision, recall and f1-score')
        pass


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








