# -*- coding: utf-8 -*-
import sys
sys.path.append("./code/util/LOU")
from community import community_louvain
sys.path.append("./code/util/convert")
import LOUconvert2 
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import networkx as nx
sys.path.append("./code/util/convert")
import LOUconvert2 
sys.path.append("./data")
import gen_plot
sys.path.append("./code/CERTIFY")
from Certify import Certify
from binarydata import all_t_marix,all_t_graph
import Gammasets
from sklearn import metrics
from matplotlib.pyplot import MultipleLocator
sys.path.append("./code/util/NMI_com")
import for_NMI
#%%
plt.rcParams['font.sans-serif']=['Simhei'] #显示中文 
plt.rcParams['axes.unicode_minus']=False #显示负号
#%%
'''
super parameter
t:timestep
n:node number
beta: noise
alpha:hypothesis test
N: number for sample
gamma: size for gammaset
'''
t=5
n=100
gamma=3
#%%
true_comm_path='./data/data/sample/comm/'
timeline_path='./data/data/sample/comm/'
data_path="./data/data/sample/comm/"
#%%
'''
get the G data and convert to matrix
'''
all_G=gen_plot.file_to_G(data_path,t,n)
x=all_t_marix(all_G)
print('------------get the matrix--------------')
print(x)

#%%
'''
get the ground truth partition
'''
print('------------get the gammasets--------------')
dic_all_t_comm=Gammasets.get_grount_truth_comm(t, true_comm_path)
tracker,rel_judge=Gammasets.get_timeline_inf(timeline_path,dic_all_t_comm)
gammasets=Gammasets.get_gammaset(t,tracker,rel_judge,gamma)

#%%
'''
for debug
'''
'''
from get_all_t import get_partition 
partition_all_t=get_partition(x,n)
true_list=for_NMI.get_true_par_list(n,t,dic_all_t_comm)
NMI=for_NMI.get_NMI(t,n,partition_all_t,true_list)
print(NMI)
'''
#%%
'''
直接对原数据NMI
'''
'''
for_NMI.plot_NMI_all_t1(t,n,all_G,true_list)
'''

#%%
print('-----------certify begin--------------------')

true_list=for_NMI.get_true_par_list(n,t,dic_all_t_comm)
for b in [0.90,0.95,0.99]:
    for attackt in [0,1,2,3,4]:
        certify=Certify(x,n,t,gammasets,true_list,beta=b,attack_t=attackt)       
        result=certify.sets_certify()
        print(result)
#%%
'''
certify=Certify(x,n,t,gammasets,true_list,beta=0.9,attack_t=4)       
result=certify.sets_certify()
print(result)
'''





'''
def getpartition(G):
    G = nx.karate_club_graph()
    node_partition = community_louvain.best_partition(G)
    #pos = nx.spring_layout(G)
    #cmap = cm.get_cmap('viridis', max(partition.values()) + 1)
    #nx.draw_networkx_nodes(G, pos, partition.keys(), node_size=40,
    #                       cmap=cmap, node_color=list(partition.values()))
    #nx.draw_networkx_edges(G, pos, alpha=0.5)
    #plt.show()
    comm_partition=LOUconvert2.LOUconvert(node_partition)
    print(node_partition)
    print(comm_partition)
    return node_partition,comm_partition

data_path="E:/18.科研/robust/dycoding/data/gen-dynamic-20161220/gen-dynamic-20161220/src/"
all_G=gen_plot.file_to_G(data_path,5,100) 
node_partition,comm_partition=getpartition(all_G[0])
#%%
num={}
num[0]=0
num[1]=0
num[0]+=1
print(num)
'''

#%%
