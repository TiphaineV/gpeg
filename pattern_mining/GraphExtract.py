from scipy import sparse
import numpy as np
import pandas as pd
import sys
from graph_bi import Graph_bi, Vertice, Vertice_usr, Vertice_mv
from graphfast import Graph
import random

class GraphExtract(Graph):
    def extract_N(self,UserId, MovieId, nbneighbors):
        print("Extracting Graph from link (",UserId,",",MovieId,") with ",nbneighbors," neighbors")
        moviesData=pd.read_csv('../Data/movies.csv')
        
        #Initialise the alphabets and the edges
        I1=[]
        I2=[]
        Erows=[]
        Ecols=[]
        Edata=[]
        
        #Setting the neighbors list
        users=list(self.colFormat.indices[self.colFormat.indptr[MovieId]:self.colFormat.indptr[MovieId+1]])
        movies=list(self.rowFormat.indices[self.rowFormat.indptr[UserId]:self.rowFormat.indptr[UserId+1]])
        
        users=users[:nbneighbors]
        movies=movies[:nbneighbors]
        
        users.append(UserId)
        movies.append(MovieId)
        
        users=list(set(users))
        movies=list(set(movies))

        #Setting Vertices
        UsersV=[]
        MoviesV=[]
        for i in range(len(users)):
            UsersV.append(Vertice(idv=i, originalId=users[i], file=moviesData, Vtype='user',
                                 movies=self.rowFormat.indices[self.rowFormat.indptr[users[i]]:self.rowFormat.indptr[users[i]+1]]))
        
        for i in range(len(movies)):
            MoviesV.append(Vertice(idv=i, originalId=movies[i], file=moviesData, Vtype='movie'))
            
          
        #Setting alphabet and edges
        for user in UsersV:
            usermv=list(self.rowFormat.indices[self.rowFormat.indptr[user.originalId]:self.rowFormat.indptr[user.originalId+1]])
            graphmv=[movie.id for movie in MoviesV if movie.originalId in usermv]
            Ecols+=graphmv
            Erows+=([user.id]*len(graphmv))
            Edata+=([1]*len(graphmv))
            I1+=user.q
        
        for movie in MoviesV:
            I2+=movie.q
            
        I1=list(set(I1))
        I2=list(set(I2))
        I=[I1,I2]
        Edges=sparse.coo_matrix((Edata, (Erows, Ecols)), shape=(int(max(Erows))+1, int(max(Ecols))+1))
        return Graph_bi(V=[UsersV,MoviesV],I=I,edges=Edges)
    
    def extract_NofN(self,UserId, MovieId, nbNeighbors, nbNofN):
        print("Extracting Graph from link (",UserId,",",MovieId,") with ",nbNeighbors," neighbors and ",nbNofN,"neighbors of neighbors")
        moviesData=pd.read_csv('../Data/movies.csv')
        
        #Initialise the alphabets and the edges
        I1=[]
        I2=[]
        Erows=[]
        Ecols=[]
        Edata=[]
        
        #Setting the neighbors list
        user_n=list(self.colFormat.indices[self.colFormat.indptr[MovieId]:self.colFormat.indptr[MovieId+1]])
        movie_n=list(self.rowFormat.indices[self.rowFormat.indptr[UserId]:self.rowFormat.indptr[UserId+1]])
        
        #Mixing the neighbors
        random.shuffle(user_n)
        random.shuffle(movie_n)
        
        #Getting nbNeighbors neighbors
        user_n=user_n[:nbNeighbors]
        movie_n=movie_n[:nbNeighbors]
        
        users=[]
        movies=[]
        
        #Setting the neighbors of neigbors 
        for user in user_n:
            mv=list(self.rowFormat.indices[self.rowFormat.indptr[user]:self.rowFormat.indptr[user+1]])
            random.shuffle(mv)
            movies+=mv[:nbNofN]
            
        for movie in movie_n:
            usr=list(self.colFormat.indices[self.colFormat.indptr[movie]:self.colFormat.indptr[movie+1]])
            random.shuffle(usr)
            users+=usr[:nbNofN]
        
        users.append(UserId)
        movies.append(MovieId)
        
        users+=user_n
        movies+=movie_n
        
        users=list(set(users))
        movies=list(set(movies))

        #Setting Vertices
        UsersV=[]
        MoviesV=[]
        for i in range(len(users)):
            UsersV.append(Vertice(idv=i, originalId=users[i], file=moviesData, Vtype='user',
                                 movies=self.rowFormat.indices[self.rowFormat.indptr[users[i]]:self.rowFormat.indptr[users[i]+1]]))
        
        for i in range(len(movies)):
            MoviesV.append(Vertice(idv=i, originalId=movies[i], file=moviesData, Vtype='movie'))
            
          
        #Setting alphabet and edges
        for user in UsersV:
            usermv=list(self.rowFormat.indices[self.rowFormat.indptr[user.originalId]:self.rowFormat.indptr[user.originalId+1]])
            graphmv=[movie.id for movie in MoviesV if movie.originalId in usermv]
            Ecols+=graphmv
            Erows+=([user.id]*len(graphmv))
            Edata+=([1]*len(graphmv))
            I1+=user.q
        
        for movie in MoviesV:
            I2+=movie.q
            
        I1=list(set(I1))
        I2=list(set(I2))
        I=[I1,I2]
        Edges=sparse.coo_matrix((Edata, (Erows, Ecols)), shape=(int(max(Erows))+1, int(max(Ecols))+1))
        return Graph_bi(V=[UsersV,MoviesV],I=I,edges=Edges)
    
    def extract(self, UserId, MovieId, threshold):
        print("Extracting Graph from link (", UserId,",", MovieId,") with node of less then", threshold,"degree")
        moviesData=pd.read_csv('../Data/movies.csv')
        
        #Initialise the alphabets and the edges
        I1=[]
        I2=[]
        Erows=[]
        Ecols=[]
        Edata=[]
        
        #Setting the neighbors list
        user_n=[user for user in list(self.colFormat.indices[self.colFormat.indptr[MovieId]:self.colFormat.indptr[MovieId+1]]) 
                if ((self.rowFormat.indptr[user+1]-self.rowFormat.indptr[user])<threshold)]
        movie_n=[movie for movie in list(self.rowFormat.indices[self.rowFormat.indptr[UserId]:self.rowFormat.indptr[UserId+1]])
                if ((self.colFormat.indptr[movie+1]-self.colFormat.indptr[movie])<threshold)]
        
        
        users=[]
        movies=[]
        
        #Setting the neighbors of neigbors 
        for user in user_n:
            mv=list(self.rowFormat.indices[self.rowFormat.indptr[user]:self.rowFormat.indptr[user+1]])
            movies+=mv
            
        for movie in movie_n:
            usr=list(self.colFormat.indices[self.colFormat.indptr[movie]:self.colFormat.indptr[movie+1]])
            users+=usr 
        
        
        users+=user_n
        movies+=movie_n
        
        users=list(set(users))
        movies=list(set(movies))
        
        #Removing nodes with a degree too high
        m=0    
        while m<len(movies):
            if (self.colFormat.indptr[movies[m]+1]-self.colFormat.indptr[movies[m]])<threshold:
                m+=1
            else:
                movies.pop(m)
        
        u=0
        while u<len(users):
            if ((self.rowFormat.indptr[users[u]+1]-self.rowFormat.indptr[users[u]])<threshold):
                u+=1
            else:
                users.pop(u)
                    
        users.append(UserId)
        movies.append(MovieId)
        
        users=list(set(users))
        movies=list(set(movies))

        #Setting Vertices
        UsersV=[]
        MoviesV=[]
        for i in range(len(users)):
            UsersV.append(Vertice_usr(idv=i, originalId=users[i], file=moviesData,
                                movies=self.rowFormat.indices[self.rowFormat.indptr[users[i]]:self.rowFormat.indptr[users[i]+1]]))

        for i in range(len(movies)):
            MoviesV.append(Vertice_mv(idv=i, originalId=movies[i], file=moviesData))
            
          
        #Setting alphabet and edges
        for user in UsersV:
            usermv=list(self.rowFormat.indices[self.rowFormat.indptr[user.originalId]:self.rowFormat.indptr[user.originalId+1]])
            graphmv=[movie.id for movie in MoviesV if movie.originalId in usermv]
            Ecols+=graphmv
            Erows+=([user.id]*len(graphmv))
            Edata+=([1]*len(graphmv))
            I1+=user.q
        
        for movie in MoviesV:
            I2+=movie.q
            
        I1=list(set(I1))
        I2=list(set(I2))
        I=[I1,I2]
        
        test=[i for i in range(len(Erows)) if ((Ecols[i]==MovieId)&(Erows[i]==UserId))]
        if len(test)==0:
            Ecols+=[i for i in range(len(movies)) if movies[i]==MovieId]
            Erows+=[i for i in range(len(users)) if users[i]==UserId]
            Edata.append(1)
            Origines=(Erows[len(Erows)-1],Ecols[len(Ecols)-1])
        
        else:
            Origines=(Erows[test[0]],Ecols[test[0]])
            
        Edges=sparse.coo_matrix((Edata, (Erows, Ecols)), shape=(len(UsersV), len(MoviesV)))
        return Graph_bi(V=[UsersV,MoviesV],I=I,edges=Edges,origines=Origines)