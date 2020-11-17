#%% Modules
#standard
import collections
import numpy as np
import numpy.random as rd
import matplotlib.pyplot as plt

#personal
from node import UserNode, MovieNode
from graph import Graph
from context import ratings, movies, tags

#%% First recommendation system
class RecSystem1(Graph):
    def __init__(self):
        super().__init__()
        pass

    def similarity(self, user: UserNode , simUser: UserNode)->float:
        '''
        UserNode metric
        '''
        try:
            return len(set(simUser.ratings.keys()).difference(set(user.ratings.keys()))) / len(user.ratings)
        except ZeroDivisionError:
            print('user has no rating')
            raise
            
    def similar_users(self,userId: int, threshold: float)->set:
        '''
        get similar users of candidate user
        '''
        user = self.get_userNode(userId)
        simUsersId = set()
        for simUser in self.userNodes:
            if simUser.nodeId != userId:
                score = self.similarity(user,simUser)
                if score > threshold:
                    simUsersId.add(simUser.nodeId)
        return simUsersId
    
    def recommend_movie(self,userId: int, threshold: float)->(MovieNode,int):
        '''
        recommend most watched movies among similar users not already seen
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


class ResultsRS1:
    '''
    useful class to show results of the first recommender system
    '''
    def __init__(self):
        self.userId = 50
        self.rs1 = RecSystem1()
    
    def show_threshold_influence(self):
        '''
        displays similar users as an histogram over all users
        '''
        thrValues = np.arange(0.2,1,0.1)
        for threshold in thrValues:
            plt.figure('Users similar to {} for thr = {}'.format(self.userId,str(threshold)[:3]))
            plt.hist(self.rs1.similar_users(self.userId,threshold),bins = 1000)
            plt.show()
        pass

    def show_recommended_movie(self, userId: int, threshold:float):
        '''
        print recommended movie in the console
        '''
        movie, nbRec = self.rs1.recommend_movie(userId = userId, threshold = threshold)
        print('Recommended movie')
        print(str(movie))
        print('Number of recommendations', nbRec)
        pass

    def show_similar_users(self, threshold: float):
        '''
        show 3 similar users in the console
        '''
        userId = self.userId
        rs1 = self.rs1

        # -- Retrieving some similar users
        user = rs1.get_userNode(userId)
        simUsers = list(rs1.similar_users(userId, threshold))
        simUser1 = rs1.get_userNode(rd.choice(simUsers))
        simUser2 = rs1.get_userNode(rd.choice(simUsers))
        simUser3 = rs1.get_userNode(rd.choice(simUsers))

        # -- Displaying results in the console
        print('User {}'.format(userId))
        print(str(UserNode(userId)))
        print('Some users similar to the candidate: \n')
        print(str(simUser1) + '\n sim. score: ' + str(rs1.similarity(user,simUser1))[:3])
        print(str(simUser2) + '\n sim. score: ' + str(rs1.similarity(user,simUser2))[:3])
        print(str(simUser3) + '\n sim. score: ' + str(rs1.similarity(user,simUser3))[:3])
        pass
    
  
if __name__ == '__main__':
    res = ResultsRS1()
    res.show_recommended_movie(50,0.9)
    res.show_threshold_influence()

