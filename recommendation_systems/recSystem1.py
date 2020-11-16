#%% Modules
#standard
import collections

#personal
from node import UserNode, MovieNode
from graph import Graph
from context import ratings, movies, tags

#%% First recommendation system
class RecSystem1(Graph):
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
        recommend most watched movies of similar users not already seen
        '''
        userRatings = self.get_userNode(userId).ratings
        simUsersId = self.similar_users(userId, threshold)
        count = collections.Counter()
        for nodeId in simUsersId:
            simUser = self.get_userNode(nodeId)
            count.update(set(simUser.ratings.keys()).difference(set(userRatings.keys())))
        
        recMovieId = count.most_common(1)[0][0]
        nbRec = count.most_common(1)[0][1]
        return self.get_movieNode(recMovieId), nbRec
    pass

if __name__ == '__main__':
    recSyst = RecSystem1()
    movie, nbRec = recSyst.recommend_movie(userId = 2, threshold = 0.2)
    print('Recommended movie')
    print(str(movie))
    print('Number of rec', nbRec)
