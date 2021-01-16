from abc import ABC, abstractmethod
import numpy as np
import copy
import matplotlib.pyplot as plt
import networkx as nwx

class Vertice:
    def __init__(self,idv:int,q:list):
        self.id=idv
        self.q=q
        self.degree=0
        
class Edge:
    def __init__(self, V1Id:int, V2Id:int):
        self.V1Id = V1Id
        self.V2Id = V2Id
        
        
class Graph_bi:
    def __init__(self, V:list, I:list, edges:list):
        self.V=V #set of Vetices 
        self.I=I #set of labels constituing patterns
        self.edges=edges
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
        for i in self.V:
            for v in i:
                v.degree = 0
                
        for v in self.V[0]:
            for e in self.edges:
                if v.id == e.V1Id:
                    v.degree +=1
                    
        for v in self.V[1]:
            for e in self.edges:
                if v.id == e.V2Id:
                    v.degree +=1
                            
        pass
        
    def interior(self,h:int,a:int):
        '''Calculate the h-a BHA-core of the graphe. It remove the vertices from V1 (resp. V2) if its degree is less 
                than h (resp. a).
        '''
        self.setDegrees()
        edges=[]
        V1=[]
        V2=[]
        for v in self.V[0]:
            if v.degree >= h:
                for e in self.edges:
                    if v.id == e.V1Id:
                        edges.append(e)
                V1.append(v)        
        self.edges=edges
        edges=[]
        for v in self.V[1]:
            if v.degree >= a:
                for e in self.edges:
                    if v.id == e.V2Id:
                        edges.append(e)
                V2.append(v)
                
        self.edges=edges
        self.V=[V1,V2]
        self.setDegrees()
        self.setCorePattern()
               
        pass
    
    def extension(self,q):
        '''Calculate the support of q, i.e. the nodes which pattern contains q
        '''
        S1=[]
        S2=[]
        edges=[]
        for v in self.V[0]:
            if ([value for value in q[0] if value in v.q]==q[0]):
                S1.append(v)
                for e in self.edges:
                    if v.id == e.V1Id:
                        edges.append(e)
        edges2=[]
        for v in self.V[1]:
            if ([value for value in q[1] if value in v.q]==q[1]):
                S2.append(v)
                for e in edges:
                    if v.id == e.V2Id:
                        edges2.append(e)
            
        S=[S1,S2]
        self.V=S
        self.edges=edges2
        self.setCorePattern()
        self.setDegrees()
        pass
    
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
    
    def Enumerate(self,EL:list,s:int,h:int,a:int):
        self.Output()
        for x in self.minus(self.q):
            print(x)
            p=self.add(self.q,x)
            Test=copy.deepcopy(self)
            Test.extension(p)
            Test.interior(h,a)
            if (len(Test.V[0])>=s)&(len(Test.V[1])>=s):
                #self.setCorePattern()
                if x not in EL:
                    self=copy.deepcopy(Test)
                    EL.append(x)
                    self.Enumerate(EL=EL,s=s,h=h,a=a)
            Test=None
                    
    def toStringPattern(self,q):
        string=''
        for i in q:
            string+=i
        return string

    def Output(self):
        #s=toStringPattern(self.q)
        print('Core pattern: ',self.q)
        G1 = nwx.Graph()
        nodelist=[]
        labels={}
        ids={}
        idx=0
        for v in self.V[0]:
            ids[str(v.id)+'V1']=idx
            G1.add_node(idx,bipartite=0)
            nodelist.append(idx)
            string=''
            for i in v.q:
                string+=str(i)
            labels[idx]=string
            idx+=1

        for v in self.V[1]:
            ids[str(v.id)+'V2']=idx
            G1.add_node(idx,bipartite=1)
            nodelist.append(idx)
            string=''
            for i in v.q:
                string+=str(i)
            labels[idx]=string
            idx+=1

        for e in self.edges:
            G1.add_edge(ids[str(e.V1Id)+'V1'],ids[str(e.V2Id)+'V2'])
    
        top = nwx.bipartite.sets(G1)[0]
        pos = nwx.bipartite_layout(G1,top)
        nwx.draw_networkx_nodes(G1,pos,nodelist=nodelist[:len(self.V[0])],node_color='c')
        nwx.draw_networkx_nodes(G1,pos,nodelist=nodelist[len(self.V[0]):],node_color='y')
        nwx.draw_networkx_edges(G1,pos)
        nwx.draw_networkx_labels(G1, pos, labels, font_size=16)

        plt.show() 
            
             
    def getVerticeV1(self,idv:int):
        pass
    
    def getVerticeV2(self,idv:int):
        pass
    
    
    
