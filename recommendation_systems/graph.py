#%% Modules
# standard
import time
import pandas as pd
import numpy as np
from types import GeneratorType
# personal
from context import ratings, movies, tags
from node import UserNode, MovieNode

#%% Graph class
class Graph:
    def __init__(self):
        self.nbUsers = ratings['userId'].max()
        self.movieIds = movies['movieId']
        print('Creating graph. Can take up to a minute')
        self.set_userNodes()
        self.set_movieNodes()
        pass

    def set_userNodes(self):
        print('Computing user nodes ...')
        t0 = time.time()

        userNodes = []
        nbUsers = self.nbUsers
        for userId in range(1,nbUsers+1):
            userNodes.append(UserNode(userId))

        print('Done ({} s.)'.format(int(time.time() - t0)))
        self.userNodes = userNodes
        pass

    def set_movieNodes(self):
        print('Computing movie nodes ...')
        t0 = time.time()

        movieNodes = []
        movieIds = self.movieIds
        for movieId in movieIds:
            movieNode = MovieNode(movieId)
            if movieNode.ratings != None: #0 degree nodes not taken into account
                movieNodes.append(MovieNode(movieId))

        print('Done ({} s.)'.format(int(time.time() - t0)))
        self.movieNodes = movieNodes
        pass

    def get_userNode(self, userId:int)->UserNode:
        try:
            return self.userNodes[userId -1]
        except IndexError:
            print('userId {} is not in the possible ids'.format(userId))
            raise
        pass

    def get_movieNode(self, movieId:int)->MovieNode:
        '''
        first get the index of the movieNode in the movieNodes list
        '''
        try:
            movieIds = self.movieIds
            idx = movieIds.index[movieIds == movieId][0]
            return self.movieNodes[idx]
        except IndexError:
            print('movieId {} is not in the possible ids'.format(movieId))
            raise
        pass

    def get_nbEdges(self) -> int:
        '''
        returns the number of edges in the graph
        '''
        return sum( userNode.degree for userNode in self.userNodes )

    def get_genEdges(self)->GeneratorType:
        '''
        makes a generator that yields the graph edges

        Returns
        -------
            generator data of form (userId, movieId, movieRating)
        '''
        return ( (userNode.nodeId, key, userNode.ratings[key])
                    for userNode in self.userNodes
                    for key in userNode.ratings.keys() )

    def get_Edges(self)->list:
        '''
        Returns
        -------
            graph edges as a list. (userId, movieId, movieRating)
        '''

        return [ (userNode.nodeId, key, userNode.ratings[key])
                    for userNode in self.userNodes
                    for key in userNode.ratings.keys() ]

    # -- Display methods
    def display_users_degree_dst(self, bins = 50, degRange = (0,500)):
        '''
        Displays the histogram of the user nodes degrees.
        '''
        degrees = [ userNode.degree for userNode in self.userNodes ]
        plt.hist(degrees, bins = bins, range = degRange)
        plt.show()
        pass

    def display_users_avgRating_dst(self, bins =50):
        '''
        Displays the histogram of the users average movie rating.
        '''
        avgRatings = [ userNode.avgRating for userNode in self.userNodes ]
        plt.hist(avgRatings, bins = bins)
        plt.show()
        pass

    def display_movie_degree_dst(self, bins = 50, degRange = (0,500)):
        '''
        Displays the histogram of the user nodes degrees.
        '''
        degrees = [ movieNode.degree for movieNode in self.movieNodes ]
        plt.hist(degrees, bins = bins, range = degRange)
        plt.show()
        pass

    def display_movie_avgRating_dst(self, bins =50):
        '''
        Displays the histogram of the users average movie rating.
        '''
        avgRatings = [ movieNode.avgRating for movieNode in self.userNodes ]
        plt.hist(avgRatings, bins = bins)
        plt.show()
        pass
    pass

if __name__ == '__main__':
    graph = Graph()
    print(next(iter(graph.get_genEdges())))

