#%% Modules
#standard
import collections

#personal
from node import UserNode, MovieNode
from graph import Graph
from context import ratings, movies, tags

#%% First recommendation system
class RecSystem2(Graph):
    def __init__(self):
        super().__init__()
        pass
    
    def similar_users(self,userId: int, threshold: int)->set:
        userRatings = self.get_userNode(userId).ratings
        simUsersId = set()
        for simUser in self.userNodes:
            if simUser.nodeId != userId:
                try:
                    score = len(set(simUser.ratings.keys()).difference(set(userRatings.keys()))) / len(userRatings)
                except TypeError:
                    print(userRatings)
                    print('User Id: ', userId)
                    print(str(simUser))
                if score > threshold:
                    simUsersId.add(simUser.nodeId)
        return simUsersId
    
    def recommend_movie(self,userId: int, threshold: int)->(MovieNode,int):
        '''
        recommend best rated movie among similar users
        '''
        userRatings = self.get_userNode(userId).ratings
        simUsersId = self.similar_users(userId, threshold)
        count = collections.Counter()
        summ = dict()
        for nodeId in simUsersId:
            simUser = self.get_userNode(nodeId)
            movieKeys = set(simUser.ratings.keys()).difference(set(userRatings.keys()))
            count.update(movieKeys)
            for key in movieKeys:
                if key in summ.keys():
                    summ[key] += simUser.ratings[key]
                else:
                    summ[key] = simUser.ratings[key]

        try:
            for key in summ.keys():
                summ[key]*= 1/count[key]

        except ZeroDivisionError:
            print('Error handling movie count')
            raise

        recMovieId = max(summ, key = summ.get)
        avgRating = max(summ.values())
        return self.get_movieNode(recMovieId), avgRating
    pass

if __name__ == '__main__':
    recSyst = RecSystem2()
    movie, avgRating = recSyst.recommend_movie(userId = 2, threshold = 0.2)
    print('Recommended movie')
    print(str(movie))
    print('Average rating among similar users', avgRating)
