from scipy import sparse
import numpy as np
import pandas as pd
import sys
from graph_bi import Graph_bi, Vertice
from graphfast import Graph

class GraphExtract(Graph):
    def extract(self,UserId, MovieId, nbneighbors):
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
