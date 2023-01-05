# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
import sys
from community import community_louvain
sys.path.append("./code/util/LOU/community")
#import matplotlib.cm as cm
#import matplotlib.pyplot as plt
import networkx as nx
sys.path.append("./code/util/convert")
import LOUconvert2 
#import numpy as np
#%%
def getpartition(G):
    #G = nx.karate_club_graph()
    node_partition = community_louvain.best_partition(G)
    #pos = nx.spring_layout(G)
    #cmap = cm.get_cmap('viridis', max(partition.values()) + 1)
    #nx.draw_networkx_nodes(G, pos, partition.keys(), node_size=40,
    #                       cmap=cmap, node_color=list(partition.values()))
    #nx.draw_networkx_edges(G, pos, alpha=0.5)
    #plt.show()
    comm_partition=LOUconvert2.LOUconvert(node_partition)
    return node_partition,comm_partition
def get_partition(graph_matrix,node_number):
    partition=[]
    clen=graph_matrix.shape[0]
    nodes=list(range(node_number))
    for i in range(graph_matrix.shape[1]):
        bi=graph_matrix[:,i]
        G=nx.Graph()
        G.add_nodes_from(nodes)
        node_id1=0
        node_id2=0
        flag=node_number-1
        num=0
        for j in bi:
            if num>=flag:
                node_id1+=1;
                node_id2=node_id1+1
                flag-=1
                num=1
            else:
                node_id2+=1
                num+=1
            if j==1:
                G.add_edge(node_id1, node_id2)
        #print(G.edges())
        node_partition,comm_partition=getpartition(G)
        partition.append(node_partition)
    return partition
#%%
'''
bi=[1,0,0]
node_id1=0
node_id2=0
flag=3-1
num=0
for j in bi:
    if num>=flag:
        node_id1+=1;
        node_id2=node_id1+1
        flag-=1
        num=0
    else:
        node_id2+=1
        num+=1
        if j==1:
            print(node_id1)
            print(node_id2)
'''