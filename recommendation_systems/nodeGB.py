'''
Nodes Classes
    A Node Class (User Node, Movie Node, Book Node, ...) should inherit the abstract _Node Class. 
    A Node Class stores as a dict its links with other vertices (the graph edges). 
'''

#%% Modules
# standard
from abc import ABC, abstractmethod
import json
#personal
from contextGB import books, reviews, interactions

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
    def set_avgRating(self):
        pass
    pass

class UserNode(__Node):
    def __init__(self,nodeId:int,userId:'str'):
        super().__init__(nodeId)
        self.userId = userId
        self.set_ratings_from_db()
        self.set_avgRating()
        self.set_degree()
        pass

    def __str__(self)->str:
        return 'id: {}, userId{} , degree: {}, avgRating: {} \n ratings: \n {}'.format(self.nodeId, self.userId, self.degree, self.avgRating, self.ratings)


    def set_ratings_from_db(self):
        '''
        {book_id : userRating}
        '''
        userRatings={}
        extract = [ (x['book_id'],x['rating']) for x, x in enumerate(interactions) if (x['user_id'] == self.userId)]
        for i in extract:
            userRatings.update({i[0]:i[1]})
        if userRatings== {}:
            self.ratings = None
        else:
            self.ratings = userRatings
        pass


    def set_degree(self):
        if self.ratings == None:
            self.degree = 0
        else:
            self.degree = len(self.ratings)

    def set_avgRating(self):
        if self.ratings != None:
            try:
                #print(self.ratings)
                self.avgRating = sum(self.ratings.values())/len(self.ratings)
            except ZeroDivisionError:
                print('len ratings is zero')
                print(str(self))
        else:
            self.avgRating = None
        pass

    def get_booksRead(self)->list:
        return list(self.ratings.keys())
    pass

class BookNode(__Node):
    def __init__(self,nodeId:int,bookId:'str'):
        super().__init__(nodeId)
        self.bookId = bookId
        self.set_title_from_db()
        self.set_authors_from_db()
        self.set_ratings_from_db()
        self.set_avgRating()
        self.set_degree()
        pass

    def __str__(self):
        return 'id: {}, bookId{}, title: {}, \n ratings: \n {}'.format(self.nodeId, self.bookId, self.title, self.ratings)
    

    def set_title_from_db(self):
        i=0
        found=False
        while(found==False & i<len(books)):
            if books[i]['book_id']==self.bookId:
                found=True
            i+=1
        if found==True:
            self.title=books[i]['title']
        else:
            raise ValueError
        pass
    
    def set_authors_from_db(self):
        i=0
        found=False
        while(found==False & i<len(books)):
            if books[i]['book_id']==self.bookId:
                found=True
            i+=1
        if found==True:
            self.authors=books[i]['authors']
        else:
            raise ValueError
        pass

    def set_ratings_from_db(self):
        bookRatings={}
        extract = [(x['user_id'],x['rating']) for x, x in enumerate(interactions) if (x['book_id'] == self.bookId)]
        for i in extract:
            bookRatings.update({i[0]:i[1]})
        #print(bookRatings.values())
        if bookRatings == {}:
            self.ratings = None
        else:
            self.ratings = bookRatings
        pass


    def set_avgRating(self):
        # there are no books without rating
        if self.ratings != None:
            try:
                #print(self.ratings)
                self.avgRating = sum(self.ratings.values())/len(self.ratings)
            except ZeroDivisionError:
                print('len ratings is zero')
                print(str(self))
        else:
            self.avgRating = None
        pass
    
    def set_degree(self):
        if self.ratings == None:
            self.degree = 0
        else:
            self.degree = len(self.ratings)

    def get_avgRating(self):
        return self.avgRating
    pass

if __name__ == '__main__':
    print(str(BookNode(1,'16037549')))
    print(str(UserNode(1,'8842281e1d1347389f2ab93d60773d4d')))
