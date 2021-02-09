"""Implémentation de graphe pour tester le pattern mining"""

from graph_bi import Vertice, Graph_bi
from GraphExtract import GraphExtract
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
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
print("Graph extracted in ",s1-s0," s")
print("We will call this graph g100 (because we took 100 neighbors)\n")

print("\nExtracting graph: ")
s0=time.time()
g5NofN=graph.extract_NofN(4,899,5,5)
s1=time.time()
print("Graph extracted in ",s1-s0," s")
print("We will call this graph g10NofN (because we took the 5 neighbors of the 5 neighbors)\n")

print("\nExtracting graph: ")
s0=time.time()
g10NofN=graph.extract_NofN(4,899,10,10)
s1=time.time()
print("Graph extracted in ",s1-s0," s")
print("We will call this graph g10NofN (because we took the 10 neighbors of the 10 neighbors)\n")

print("\nExtracting graph: ")
s0=time.time()
g100NofN=graph.extract_NofN(4,899,100,100)
s1=time.time()
print("Graph extracted in ",s1-s0," s")
print("We will call this graph g100NofN (because we took the 100 neighbors of the 100 neighbors)\nWe just extract it out of curiosity, this graph will not be enumerated\n")

print("Cleaning previous pdf")
! ./cleaning.sh
print("Cleaned\n")

print("\nEnumerating g10 with h=a=2 ")
s0=time.time()
with PdfPages('10n_h=2_a=2.pdf') as pdf:
    g10.Enumerate(EL=[],s=1,h=2,a=2,pdf=pdf)
s1=time.time()
print("Graph enumerated in ",s1-s0," s\n")

print("\nEnumerating g100 with h=a=4")
s0=time.time()
with PdfPages('100n_h=4_a=4.pdf') as pdf:
    g100.Enumerate(EL=[],s=1,h=4,a=4,pdf=pdf)
s1=time.time()
print("Graph enumerated in ",s1-s0," s\n")   

print("\nEnumerating g5NofN with h=a=2 ")
s0=time.time()
with PdfPages('5NofN_h=2_a=2.pdf') as pdf:
    g5NofN.Enumerate(EL=[],s=1,h=2,a=2,pdf=pdf)
s1=time.time()
print("Graph enumerated in ",s1-s0," s\n")

print("\nEnumerating g10NofN with h=a=4")
s0=time.time()
with PdfPages('10NofN_h=4_a=4.pdf') as pdf:
    g10NofN.Enumerate(EL=[],s=1,h=4,a=4,pdf=pdf)
s1=time.time()
print("Graph enumerated in ",s1-s0," s\n")  