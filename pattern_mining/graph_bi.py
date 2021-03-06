from abc import ABC, abstractmethod
import numpy as np
import copy
import matplotlib.pyplot as plt
import networkx as nwx
import scipy.sparse as sparse


class Vertice:
    def __init__(self,idv:int,originalId:int,file,Vtype:str,movies=None):
        self.id=idv
        self.originalId=originalId
        self.degree=0
        self.Vtype=Vtype
        self.setPattern(file,movies)
        if self.Vtype=='movie':
            self.setTitle(file)
        
    def setPattern(self,file,movies):
        if self.Vtype=='user':
            if movies.any():
                self.q=[]
                genres=[genre.split('|') for genre in file[file['movieId'].isin(movies)]['genres']]
                for g in genres:
                    self.q+=g
                self.q=list(set(self.q))

            
        elif self.Vtype=='movie':
            self.q=[]
            genres=[genre.split('|') for genre in file[file['movieId'].isin([self.originalId])]['genres']]
            for g in genres:
                self.q+=g
            self.q=list(set(self.q))
            
        for i in range(len(self.q)):
            self.q[i]=self.q[i]+'_'+self.Vtype
    
    def setTitle(self,file):
         self.title=file[file['movieId'].isin([self.originalId])]['title'].mode()[0]
        
        

class Graph_bi:
    def __init__(self, V:list, I:list, edges):
        self.V=V #set of Vetices 
        self.I=I #set of labels constituing patterns
        self.edges=edges
        self.rowFormat = sparse.csr_matrix(self.edges)
        self.colFormat = sparse.csc_matrix(self.edges)
        self.q=[]
        self.setCorePattern()
        self.setDegrees()
        
    def setCorePattern(self):
        '''Calculate the core bi-pattern, i.e. the more specific patttern that occurs in the nodes.
        '''
        q1=self.I[0]
        q2=self.I[1]
        for v in self.V[0]:
            q1=[value for value in q1 if value in v.q]
        for v in self.V[1]:
            q2=[value for value in q2 if value in v.q]
        q=[q1,q2]
        self.q=q
        pass
    
    def setDegrees(self):
        '''Set the degree of each vertice, i.e. the number of connexion to the other vertices it has.
        '''
        self.minD=[self.rowFormat.indptr[self.V[0][0].id+1]-self.rowFormat.indptr[self.V[0][0].id],
                   self.colFormat.indptr[self.V[1][0].id+1]-self.colFormat.indptr[self.V[1][0].id]]
        for v in self.V[0]:
            v.degree=self.rowFormat.indptr[v.id+1]-self.rowFormat.indptr[v.id]
            if len(self.minD)==0:
                sel
            if (v.degree<self.minD[0]):
                self.minD[0]=v.degree
            
        for v in self.V[1]:
            v.degree=self.colFormat.indptr[v.id+1]-self.colFormat.indptr[v.id]
            if (v.degree<self.minD[1]):
                self.minD[1]=v.degree                
        pass
        
    def interior(self,h:int,a:int):
        '''Calculate the h-a BHA-core of the graphe. It remove the vertices from V1 (resp. V2) if its degree is less 
                than h (resp. a).
        '''
        self.setDegrees()

        while (self.minD[0] < h)|(self.minD[1] < a):
            S1=[]
            S2=[]
            
            for v in self.V[0]:
                if v.degree >= h:
                    S1.append(v)

                    
            for v in self.V[1]:
                if v.degree >= a:
                    S2.append(v)
            
            erows=[]
            ecols=[]
            edata=[]
            
            for v in S1:
                links=list(self.rowFormat.indices[self.rowFormat.indptr[v.id]:self.rowFormat.indptr[v.id+1]])
                graphv=[v.id for v in S2 if v.id in links]
                ecols+=graphv
                erows+=([v.id]*len(graphv))
                edata+=([1]*len(graphv))

            if (len(erows)==0)|(len(ecols)==0):
                return False
            
            self.edges=sparse.coo_matrix((edata, (erows, ecols)), shape=(int(max(erows))+1, int(max(ecols))+1))
            self.rowFormat = sparse.csr_matrix(self.edges)
            self.colFormat = sparse.csc_matrix(self.edges)
            self.V=[[v for v in S1 if v.id in list(set(erows))],[v for v in S2 if v.id in list(set(ecols))]]
            self.setDegrees()
    

        self.setCorePattern()
        return True         
    
    def extension(self,q):
        '''Calculate the support of q, i.e. the nodes which pattern contains q
        '''
        erows=[]
        ecols=[]
        edata=[]
        for v in self.V[0]:
            if ([value for value in q[0] if value in v.q]==q[0]):
                ecols+=list(self.rowFormat.indices[self.rowFormat.indptr[v.id]:self.rowFormat.indptr[v.id+1]])
                erows+=([v.id]*v.degree)
                edata+=([1]*v.degree)
        
        if (len(erows)==0)|(len(ecols)==0):
            return False
            
        V2=[v for v in self.V[1] if v.id in list(set(ecols))]
        edges= sparse.coo_matrix((edata, (erows, ecols)), shape=(int(max(erows))+1, int(max(ecols))+1))
        colFormat = sparse.csc_matrix(edges)        
        erows=[]
        ecols=[]
        edata=[]
            
        for v in V2:
            if ([value for value in q[1] if value in v.q]==q[1]):
                erows+=list(colFormat.indices[colFormat.indptr[v.id]:colFormat.indptr[v.id+1]])
                ecols+=([v.id]*(colFormat.indptr[v.id+1]-colFormat.indptr[v.id]))
                edata+=([1]*(colFormat.indptr[v.id+1]-colFormat.indptr[v.id]))
        
        if (len(erows)==0)|(len(ecols)==0):
            return False
            
        self.edges=sparse.coo_matrix((edata, (erows, ecols)), shape=(int(max(erows))+1, int(max(ecols))+1))
        self.rowFormat = sparse.csr_matrix(self.edges)
        self.colFormat = sparse.csc_matrix(self.edges)    
        self.V=[[v for v in self.V[0] if v.id in list(set(erows))],[v for v in V2 if v.id in list(set(ecols))]]
            
        self.setCorePattern()
        self.setDegrees()
        return True
    
    def minus(self,q:list):
        "Return the set of item from the alphabet I which is not in the pattern q"
        minus=[value for value in self.I[0]+self.I[1] if (value not in q[0]) & (value not in q[1])]
        return minus
    
    def add(self,q:list,x):
        "Return the pattern q with x added in the right place"
        q_new=copy.deepcopy(q)
        if x in self.I[0]:
            q_new[0] += [x]
        else:
            q_new[1] += [x]
            
        return q_new
    
    def Enumerate(self,EL:list,s:int,h:int,a:int,pdf=None):
        self.Output(pdf)
        for x in self.minus(self.q):
            p=self.add(self.q,x)
            Test=copy.deepcopy(self)
            is_connected=Test.extension(p)
            if is_connected:
                is_connected=Test.interior(h,a)
                if is_connected:
                    if (len(Test.V[0])>=s)&(len(Test.V[1])>=s):
                        if x not in EL:
                            self=copy.deepcopy(Test)
                            EL.append(x)
                            self.Enumerate(EL=EL,s=s,h=h,a=a,pdf=pdf)
            Test=None
                    


    def Output(self,pdf=None):
            #s=toStringPattern(self.q)
            #print('\nCore pattern: ',self.q,'\n')
            G1 = nwx.Graph()
            nodelist=[]
            labels={}
            ids={}
            idx=0
            for v in self.V[0]:
                ids[str(v.id)+'V1']=idx
                G1.add_node(idx,bipartite=0)
                nodelist.append(idx)
                labels[idx]=str(v.id)
                idx+=1

            for v in self.V[1]:
                ids[str(v.id)+'V2']=idx
                G1.add_node(idx,bipartite=1)
                nodelist.append(idx)
                labels[idx]=v.title
                idx+=1

            for i in range(len(self.edges.row)):

                G1.add_edge(ids[str(self.edges.row[i])+'V1'],ids[str(self.edges.col[i])+'V2'])
                
                
            
                
            fig=plt.figure(figsize=(3,3))
            
            top_nodes = {n for n, d in G1.nodes(data=True) if d["bipartite"] == 0}
            bottom_nodes = set(G1) - top_nodes
            pos = nwx.bipartite_layout(G1,top_nodes)
            nwx.draw_networkx_nodes(G1,pos,nodelist=nodelist[:len(self.V[0])],node_color='c',node_size=8)
            nwx.draw_networkx_nodes(G1,pos,nodelist=nodelist[len(self.V[0]):],node_color='y',node_size=8)
            nwx.draw_networkx_edges(G1,pos,width=0.02)
            nwx.draw_networkx_labels(G1, pos, labels, font_size=1.5)


            if pdf==None:
                print('\nCore pattern: ',self.q,'\n')
                plt.show()

            else:
                ax=None
                String='Core Pattern:\n'
                
                for i in range(len(self.q)):
                    c=0
                    if i==0:
                        String+='User: '
                    else:
                        String+='Movie: '
                    for q in self.q[i]:
                        String+=" '"+q+"'"+","
                        c+=1
                        if c == 9:
                            c=0
                            String+="\n"
                    String+='\n'

                ax=fig.add_subplot()
                ax.set_title(String, fontsize=2.4)
                ax.margins(0.15)
                pdf.savefig()
                ax=None

            plt.close()
            
            
             
    def getVerticeV1(self,idv:int):
        pass
    
    def getVerticeV2(self,idv:int):
        pass
    
    
    
