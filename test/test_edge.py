import unittest
import numpy as np

from contextTest import Edge

class TestTags(unittest.TestCase):
    '''Tests if tags are being set properly
    '''
    def setUp(self):
        self.data = [{
                    'userId': 3000,
                    'movieId': 9999,
                    'rating': 4.0,
                    'tags': np.nan
                },
                {
                    'userId': 100,
                    'movieId': 3000,
                    'rating': 3.5,
                    'tags': ['cool', 'tres cool']
                }
        ]
        pass

    def test_nan(self):
        data = self.data
        tpl = data[0]['userId'], data[0]['movieId'], data[0]['rating'], data[0]['tags']
        edge = Edge(*tpl)
        self.assertEqual(edge.tags, [])
        pass

    def test_no_nan(self):
        data = self.data
        tpl = data[1]['userId'], data[1]['movieId'], data[1]['rating'], data[1]['tags']
        edge = Edge(*tpl)
        self.assertEqual(edge.tags, ['cool', 'tres cool'])
        pass

if __name__ == '__main__':
    unittest.main()

