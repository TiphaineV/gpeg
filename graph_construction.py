#%% Modules
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#%% Graph construction
def main():
    filePath =  "./ml-latest-small/"
    ratings = pd.read_csv(filePath + "ratings.csv")
    movies = pd.read_csv(filePath + "movies.csv")
    tags = pd.read_csv(filePath + "tags.csv")
    
    class Graph:
        def __init__(self,*args):
            ### DOES NOT work
            self.userNodes = self.compute_users()
            #self.movieNodes = self.compute_movies()
            pass
        def compute_users(self):
            userNodes = set()
            n = len(ratings)
            print('[',end='')
            for k,userId in enumerate(ratings['userId']):
                if k/n in np.arange(0,1,0.1):
                    print('#',end='')
                userNodes.add(UserNode(userId))
            print(']')
            return userNodes
        def compute_movies(self):
            movieNodes = set()
            for movieId in ratings['movieId']:
                movieNodes.add(MovieNode(movieId))
            return movieNodes
        def show_degrees(self,bins:int):
            degrees = [userNode.degree for userNode in userNodes]
            plt.hist(degrees,bins=bins)
            plt.show()
            pass

    class Node:
        def __init__(self,nodeId:int):
            self.nodeId = nodeId
            pass
        def getid(self):
            return self.nodeId
        pass

    class UserNode(Node):
        def __init__(self,nodeId:int):
            ### WORKS 
            super().__init__(nodeId)
            self.ratings = self.user_ratings_from_db()
            self.tags = self.user_tags_from_db()
            self.degree = self.compute_degree()
            self.avgRating = self.compute_average()
            #self.prefMovies = self.compute_pref()
            pass
        def user_ratings_from_db(self)->dict:
            userRatings = ratings[ratings['userId'] == self.nodeId][['movieId','rating']]
            return dict({ userRatings['movieId'].iloc[k] : userRatings['rating'].iloc[k] for k in range(len(userRatings))})
        def user_tags_from_db(self):
            userTags = tags[tags['userId'] == self.nodeId][['movieId','tag']]
            return dict({ userTags['movieId'].iloc[k] : userTags['tag'].iloc[k] for k in range(len(userTags))})
        def compute_degree(self):
            return len(ratings)
        def compute_average(self):
            return sum(self.ratings.values())/len(self.ratings)
        def compute_pref(self):
            ### NOT implemented yet
            pass
    class MovieNode(Node):
        ### NOT implemented yet
        def __init__(self,nodeId:int):
            super().__init__(nodeId)
            self.genre = self.genre_from_db()
            #self.link = self.link_from_db()
            self.name = ...
            pass
        def genre_from_db(self)->set:
            return set(movies[movies['movieId'] == self.nodeId]['genres'].to_string(index=False)[1:].split('|'))
    Graph()
    return
if __name__ == '__main__':
    main()
    