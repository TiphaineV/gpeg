"""Implémentation de graphe pour tester le pattern mining"""

from graph_bi import Vertice, Graph_bi
from GraphExtract import GraphExtract
import pandas as pd
import time

userMovieData_byChunk = pd.read_csv('../Data/userMovieData_small.csv', chunksize= int(1e6))

s0=time.time()
graph = GraphExtract(userMovieData_byChunk)
s1=time.time()
print("Graph made in ",s1-s0," s")

print("\nExtracting graph: ")
s0=time.time()
g10=graph.extract(4,899,10)
s1=time.time()
print("Graph extracted in ",s1-s0," s")
print("We will call this graph g10 (because we took 10 neighbors)\n")

print("\nExtracting graph: ")
s0=time.time()
g100=graph.extract(4,899,100)
s1=time.time()
print("Graph extracted in ",s1-s0," s\n")
print("We will call this graph g100 (because we took 100 neighbors)\n")

print("\nExtracting graph: ")
s0=time.time()
g1000=graph.extract(4,899,50000)
s1=time.time()
print("Graph extracted in ",s1-s0," s\n")
print("We will call this graph Big (because he only exists to see how much time it takes to extract the graph with 50000 neighbors)\n")
#g.Output()
#p=[['Action_user', 'Fantasy_user', 'Documentary_user', 'Drama_user', 'Musical_user', 'Romance_user', 'War_user', 'Sci-Fi_user', 'Mystery_user', 'IMAX_user', 'Film-Noir_user', 'Crime_user', 'Thriller_user', 'Horror_user', 'Animation_user', 'Comedy_user', 'Adventure_user', 'Western_user', 'Children_user'], ['Romance_movie']]

#test_ext=copy.deepcopy(g)
#text_ext.extension(p)
print("\nEnumerating g10 with h=a=2 \n")
g10.Enumerate(EL=[],s=1,h=2,a=2)

print("\nEnumerating g100 with h=a=4\n")
g100.Enumerate(EL=[],s=1,h=4,a=4)