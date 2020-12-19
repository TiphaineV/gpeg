import pandas as pd
import numpy as np

class Edge:
    def __init__(self, userId:int, movieId:int, rating: float, tags: list):
        self.userId = userId
        self.movieId = movieId
        self.rating = rating
        self.set_tags(tags)
        self.hidden = False
        pass

    def set_tags(self, tags):
        if tags is np.nan:
            self.tags = []
        else:
            self.tags = tags

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
