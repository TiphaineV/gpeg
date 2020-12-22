#%% Modules
import unittest
import numpy as np
from numpy.testing import assert_almost_equal

from contextTest import Edge, FastGraph


class TestUserFeature(unittest.TestCase):
    def setUp(self):
        # -- building the graph
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


if __name__ == '__main__':
    unittest.main()