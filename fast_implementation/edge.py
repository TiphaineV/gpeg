import pandas as pd
import numpy as np

class Edge:
    def __init__(self, userId:int, movieId:int, rating: float, tags: list, timeRtg: int, timeTags: list):
        self.userId = userId
        self.movieId = movieId
        self.rating = rating
        self.timeRtg = timeRtg
        self.set_tags(tags)
        self.set_timeTags(timeTags)
        self.hidden = False
        pass

    def set_tags(self, tags):
        '''should be a list of strings
        '''
        if tags is np.nan:
            self.tags = []
        else:
            self.tags = tags
        pass

    def set_timeTags(self, timeTags):
        '''should be a list of int
        '''
        if timeTags is np.nan:
            self.timeTags = []
        else:
            self.timeTags = timeTags
        pass

    def set_group(self, group):
        self.group = group
        pass

    def hide(self):
        self.hidden = True
        pass

    def get_userId(self):
        return self.userId

    def get_movieId(self):
        return self.movieId
