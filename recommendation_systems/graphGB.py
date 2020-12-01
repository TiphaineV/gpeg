'''
Graph Class.
    Creates all User Nodes and Movie Nodes from the dataset and stores them as lists. 
    Some display methods are also implemented to get an idea of the distribution of some nodes properties (degree, average Rating)
    Recommender systems should inherit the Graph Class.
'''

#%% Modules
# standard
import time
import json
import numpy as np
# personal
from contextGB import books, reviews, interactions
from nodeGB import UserNode, BookNode

#%% Graph class
class Graph:
    def __init__(self):
        print('Creating graph. Can take up to a minute')
        self.set_userNodes()
        self.set_bookNodes()
        pass

    def set_userNodes(self):
        print('Computing user nodes ...')
        t0 = time.time()

        userNodes = []
        users=[]
        for i in reviews:
            #we are using reviews because it is smaller than interactions and the list of users obtained is the same
            users.append(i['user_id'])
        users=list(set(users))#set() allows to get the list without repetitions
        print('Users extracted ({} s.)'.format(int(time.time() - t0)))
        for i in range(len(users)):
            userNodes.append(UserNode(i,users[i]))
            if i%500==0:
                print('Still going ({} in {} s.)'.format(i, int(time.time()-t0)))
        print('Done ({} s.)'.format(int(time.time() - t0)))
        pass

    def set_bookNodes(self):
        print('Computing book nodes ...')
        t0 = time.time()

        bookNodes = []
        books=[]
        for i in books:
            books.append(i['user_id'])
        books=list(set(books))#set() allows to get the list without repetitions
        for i in range(len(books)):
            bookNodes.append(BookNode(i,books[i]))

        print('Done ({} s.)'.format(int(time.time() - t0)))
        self.bookNodes = bookNodes
        pass

    def get_userNode_nodeId(self, nodeId:int)->UserNode:
        try:
            return self.userNodes[nodeId -1]
        except IndexError:
            print('nodeId {} is not in the possible ids'.format(nodeId))
            raise
        pass
    
    def get_userNode_userId(self, userId:'str')->UserNode:
        i=0
        found=False
        while(found==False and i<len(self.userNodes)):
            if self.userNodes[i].userId==userId:
                found=True
            i+=1
        if found:
            return self.userNodes[i]
        else:
            raise Exception('userId {} is not in the possible ids'.format(userId))
        pass

    def get_bookNode(self, bookId:int)->BookNode:
        '''
        first get the index of the BookNode in the bookNodes list
        '''
        i=0
        found=False
        while(found==False and i<len(self.bookNodes)):
            if self.bookNodes[i].bookId==bookId:
                found=True
            i+=1
        if found:
            return self.userNode[i]
        else:
            raise Exception('bookId {} is not in the possible ids'.format(bookId))
        pass

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

    def display_book_degree_dst(self, bins = 50, degRange = (0,500)):
        '''
        Displays the histogram of the user nodes degrees.
        '''
        degrees = [ bookNode.degree for bookNode in self.bookNodes ]
        plt.hist(degrees, bins = bins, range = degRange)
        plt.show()
        pass

    def display_book_avgRating_dst(self, bins =50):
        '''
        Displays the histogram of the users average movie rating.
        '''
        avgRatings = [ bookNode.avgRating for bookNode in self.bookNodes ]
        plt.hist(avgRatings, bins = bins)
        plt.show()
        pass
    pass

if __name__ == '__main__':
    graph = Graph()
