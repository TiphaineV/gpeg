class Edge:
    def __init__(self, userId:int, movieId:int, rating: float, tags: list):
        self.userId = userId
        self.movieId = movieId
        self.rating = rating
        self.tags = tags
        pass

    def set_group(self, group):
        self.group = group
        pass
