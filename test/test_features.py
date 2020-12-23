#%% Modules
import unittest
import numpy as np
from numpy.testing import assert_almost_equal

from contextTest import Edge, FastGraph, _Clf


class TestNodeFeature(unittest.TestCase):
    '''Tests if the node side works as it should
    '''
    def setUp(self):
        # -- builds the graph
        graph = FastGraph()
        params = [(uId, mId, (uId -1)*mId, ['cool']*(uId-1), uId+mId, [10*mId]*(uId-1)) 
                                    for uId in range(1,3)
                                    for mId in range(1,6)]

        edges = np.array([Edge(*tpl) for tpl in params])
        graph.edges = edges


        self.graph = graph
        pass

    def test_user_features(self):
        def average_rating(ratings, tags, timeRtg, timeTags):
            return sum(tpl[1] for tpl in ratings) / len(ratings)

        def is_tag(ratings, tags, timeRtg, timeTags):
            return float(any([len(tpl[1])>0 for tpl in tags]))

        fncts = [average_rating, is_tag]

        user1 = FastGraph.group_by_user(self.graph.edges)[1]
        user2 = FastGraph.group_by_user(self.graph.edges)[2]

        assert_almost_equal(user1.get_features(fncts), np.array([0., 0.]), err_msg= 'pb with user1 feat.')
        assert_almost_equal(user2.get_features(fncts), np.array([3., 1.]), err_msg= 'pb with user2 feat.')
        pass

    def test_movie_features(self):
        def average_rating(ratings, tags, timeRtg, timeTags, genre, imdb):
            return sum(tpl[1] for tpl in ratings) / len(ratings)

        def is_tag(ratings, tags, timeRtg, timeTags, genre, imdb):
            return float(any([len(tpl[1])>0 for tpl in tags]))

        fncts = [average_rating, is_tag]

        movie1 = FastGraph.group_by_movie(self.graph.edges)[1]
        movie4 = FastGraph.group_by_movie(self.graph.edges)[4]

        assert_almost_equal(movie1.get_features(fncts), np.array([0.5, 1.]))
        assert_almost_equal(movie4.get_features(fncts), np.array([2., 1.]))
        pass

#%% Test features, clf side
class TestClf(_Clf):
    '''Defines a clf for the purpose of the test.
    '''
    def __init__(self):
        super().__init__()
        pass

    def fit(self):
        return

    def predict(self):
        return

    def set_featFncts(self):
        def user_average_rating(ratings, tags, timeRtg, timeTags):
            return sum(tpl[1] for tpl in ratings) / len(ratings)

        def user_is_tag(ratings, tags, timeRtg, timeTags):
            return float(any([len(tpl[1])>0 for tpl in tags]))

        def movie_average_rating(ratings, tags, timeRtg, timeTags, genre, imdb):
            return sum(tpl[1] for tpl in ratings) / len(ratings)

        def movie_is_tag(ratings, tags, timeRtg, timeTags, genre, imdb):
            return float(any([len(tpl[1])>0 for tpl in tags]))

        self.featFncts = {'user': [user_average_rating, user_is_tag],
                      'edge': [],
                      'movie': [movie_average_rating, movie_is_tag]
                      }
        pass




class TestClfFeature(unittest.TestCase):
    '''Tests if the clf side works as it should
    '''
    def setUp(self):
        # -- builds the graph
        graph = FastGraph()
        params = [(uId, mId, (uId-1)*mId, ['cool']*(uId-1), uId+mId, [10*mId]*(uId-1)) 
                                    for uId in range(1,3)
                                    for mId in range(1,6)]

        edges = np.array([Edge(*tpl) for tpl in params])
        graph.edges = edges
        self.graph = graph
        self.clf = TestClf()
        pass

    def test_feature_matrix(self):
        X = self.clf._get_feature_matrix(self.graph.edges)
        xTrue = np.array([0.,  0.,  0.5, 1.,
                            0.,  0.,  1.,  1.,
                            0.,  0.,  1.5, 1.,
                            0.,  0.,  2.,  1.,
                            0.,  0.,  2.5, 1.,
                            3.,  1.,  0.5, 1.,
                            3.,  1.,  1.,  1.,
                            3.,  1.,  1.5, 1.,
                            3.,  1.,  2.,  1.,
                            3.,  1.,  2.5, 1. ]).reshape(10,4)
        
        assert_almost_equal(X,xTrue)
        pass


if __name__ == '__main__':
    unittest.main()