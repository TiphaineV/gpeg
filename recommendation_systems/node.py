#%% Modules
# standard
from abc import ABC, abstractmethod
import pandas as pd

#personal
from context import ratings, movies, tags

#%% Node classes
class __Node(ABC):
    '''
    Abstract Class Node
    '''
    def __init__(self,nodeId:int):
        self.nodeId = nodeId
        pass

    @abstractmethod
    def set_degree(self):
        pass

    @abstractmethod
    def set_ratings_from_db(self):
        pass

    @abstractmethod
    def set_tags_from_db(self):
        pass

    @abstractmethod
    def set_avgRating(self):
        pass
    pass

class UserNode(__Node):
    def __init__(self,nodeId:int):
        super().__init__(nodeId)
        self.set_ratings_from_db()
        self.set_tags_from_db()
        self.set_avgRating()
        self.set_degree()
        pass

    def __str__(self)->str:
        ''' Not implemented yet'''
        return 'id: {}, degree: {}, avgRating: {} \n ratings: \n {} tags: \n {}'.format(self.nodeId, self.degree, self.avgRating, self.ratings, self.tags)
        pass

    def set_ratings_from_db(self):
        '''
        {movieId : userRating}
        '''
        userRatings = ratings[ratings['userId'] == self.nodeId][['movieId','rating']]
        self.ratings = dict({ userRatings['movieId'].iloc[k] : userRatings['rating'].iloc[k] for k in range(len(userRatings))})
        pass

    def set_tags_from_db(self):
        '''
        {movieId : userTag}
        '''
        userTags = tags[tags['userId'] == self.nodeId][['movieId','tag']]
        self.tags = dict({ userTags['movieId'].iloc[k] : userTags['tag'].iloc[k] for k in range(len(userTags))})
        pass

    def set_degree(self):
        self.degree = len(self.ratings)
        pass

    def set_avgRating(self):
        self.avgRating = sum(self.ratings.values())/len(self.ratings)
        pass
    pass

class MovieNode(__Node):
    def __init__(self,nodeId:int):
        super().__init__(nodeId)
        self.set_title_from_db()
        self.set_genres_from_db()
        self.set_ratings_from_db()
        self.set_tags_from_db()
        self.set_avgRating()
        self.set_degree()
        pass

    def __str__(self):
        return 'id: {}, title: {}, genres: {} \n ratings: \n {}'.format(self.nodeId, self.title, self.genres, self.ratings)
    
    def set_genres_from_db(self):
        self.genres = set(movies[movies['movieId'] == self.nodeId]['genres'].to_string(index=False)[1:].split('|'))
        pass

    def set_title_from_db(self):
        title = movies[movies['movieId'] == self.nodeId]['title']
        if title.empty:
            raise ValueError
        else:
            self.title = title.to_string()
        pass

    def set_ratings_from_db(self):
        movieRatings = ratings[ratings['movieId'] == self.nodeId][['userId','rating']]
        self.ratings = dict({ movieRatings['userId'].iloc[k] : movieRatings['rating'].iloc[k] for k in range(len(movieRatings)) })
        pass

    def set_tags_from_db(self)->set:
        movieTags = tags[tags['movieId'] == self.nodeId][['userId','tag']]
        self.tags = dict({ movieTags['userId'].iloc[k] : movieTags['tag'].iloc[k].lower() for k in range(len(movieTags))})
        pass

    def set_avgRating(self):
        # some movies are not rated
        if len(self.ratings)>0:
            try:
                self.avgRating = sum(self.ratings.values())/len(self.ratings)
            except ZeroDivisionError:
                print('len ratings is zero')
                print(str(self))
        pass
    def set_degree(self):
        self.degree = len(self.ratings)
    pass

if __name__ == '__main__':
    print(str(MovieNode(1)))
    print(str(UserNode(1)))