# -*- coding: utf-8 -*-
import numpy as np
import networkx as nx
'''
    for unweighted data which w=1 for all edges
'''

def all_t_marix(all_G):
    matrix=[]
    for G in all_G:
        nodes=G.nodes()
        edges=G.edges()
        binary,a=get_binarydata(nodes,edges)
        matrix.append(list(binary))
    return np.array(matrix).T

def all_t_graph(matrix,n,t):
    fortest=[]
    for i in range(t):
        bi_data=matrix[:,i]
        nodes,edges=bi_tograph(bi_data,n)
        fortest.append((nodes,edges))
    return fortest
    
            
def get_binarydata(nodes_,edges_):
        n=len(nodes_)
        bi_len=int(n*(n-1)/2)
        bi_data=np.zeros(bi_len,dtype=int)
        for edge in edges_:
            min_=min(edge[0],edge[1])
            max_=max(edge[0],edge[1])
            index=0
            for i in range(1,min_+1):
                index+=n-i
            index+=max_-min_-1
            bi_data[index]=1
        return bi_data,n
    
def bi_tograph(bi_data,n):
        bi_len=len(bi_data)
        nodes_ = []
        for i in range(n):
            nodes_.append(i)
            i += 1
        edges_ = []
        node_id1=0
        node_id2=0
        flag=n-1
        num=0
        for i in range(bi_len):
            if num>=flag:
                node_id1+=1;
                node_id2=node_id1+1
                flag-=1
                num=1
            else:
                node_id2+=1
                num+=1
            if bi_data[i]==1:
                edges_.append((node_id1, node_id2))
        return nodes_, edges_
  
