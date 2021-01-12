"""Implémentation de graphe pour tester le pattern mining"""

from graph_class import Vertice, Edge, Graph_bi

V1=[]
V1.append(Vertice(idv=1,q=['a','b','c']))
V1.append(Vertice(idv=2,q=['a','b','d']))
V1.append(Vertice(idv=3,q=['a','b','c']))

V2=[]
V2.append(Vertice(idv=1,q=['w','x','y']))
V2.append(Vertice(idv=2,q=['w','x','z']))
V2.append(Vertice(idv=3,q=['w','x','y']))
V=[V1,V2]

edges=[]
edges.append(Edge(1,1))
edges.append(Edge(1,2))
edges.append(Edge(1,3))
edges.append(Edge(2,1))
edges.append(Edge(2,2))
edges.append(Edge(2,3))
edges.append(Edge(3,3))

I=[['a','b','c','d'],['w','x','y','z']]

G=Graph_bi(V=V,I=I,edges=edges)

EL=[]
G.Enumerate(EL=EL,s=1,h=2,a=2)
print(EL)