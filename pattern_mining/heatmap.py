from graph_bi import Vertice, Graph_bi
from GraphExtract import GraphExtract
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
import time
import subprocess
from PyPDF2 import PdfFileReader
import seaborn as sb
import matplotlib.pyplot as plt
import numpy as np
import copy

userMovieData_byChunk = pd.read_csv('../Data/userMovieData_small.csv', chunksize= int(1e6))

graph = GraphExtract(userMovieData_byChunk)

h_value=[6,8,10,12]
a_value=[6,8,10,12]
nb_pattern=np.random.random((len(h_value),len(a_value)))
size=np.random.random((len(h_value),len(a_value)))
balance=np.random.random((len(h_value),len(a_value)))
i_h=0

gOrgn=graph.extract(4,899,100)
#g=graph.extract(4,899,100)
for h in h_value:
    i_a=0
    for a in a_value:
        gOrgn_c=copy.deepcopy(gOrgn)
        #g_c=copy.deepcopy(g)
        path_orig='gOringin_h='+str(h)+'_a='+str(a)+'.pdf'
        #path='g_h='+str(h)+'_a='+str(a)+'.pdf'
        s_b=[0,0,0]
        with PdfPages(path_orig) as pdf:
            gOrgn_c.Enumerate(EL=[],s=1,h=h,a=a,pdf=pdf,mode='OriginLink',count='Size&Balance',sb=s_b)
        nb_pattern[i_h][i_a]=s_b[2]
        size[i_h][i_a]=s_b[0]
        balance[i_h][i_a]=s_b[1]
            
        '''with PdfPages(path) as pdf:
            g_c.Enumerate(EL=[],s=1,h=h,a=a,pdf=pdf)
            
        with open(path, 'rb') as f:
            pdf = PdfFileReader(f)
            nb_pattern = pdf.getNumPages() - 1'''
            
        #orginOnnormal[i_h][i_a]= nb_pattern_orig/nb_pattern
        i_a+=1
        
    i_h+=1


fig, (ax, ax2, ax3) = plt.subplots(3)
nb_hm = sb.heatmap(nb_pattern,xticklabels=a_value,yticklabels=h_value,annot=True,ax=ax)
size_hm= sb.heatmap(size,xticklabels=a_value,yticklabels=h_value,annot=True,ax=ax2)
balance_hm = sb.heatmap(balance,xticklabels=a_value,yticklabels=h_value,annot=True,ax=ax3)

ax.set_title('Number of pattern')
ax2.set_title('Size of graphs')
ax3.set_title('Balance of users and movies')

plt.ylabel('Values of h')
plt.xlabel('Values of a')
plt.show()



subprocess.call("./cleaning.sh")




