# -*- coding: utf-8 -*-
import sys
sys.path.append("./code/util/LOU")
from community import community_louvain
sys.path.append("./code/util/convert")
import LOUconvert2 
from sklearn import metrics
from matplotlib.pyplot import MultipleLocator
import matplotlib.pyplot as plt
#%%
def get_true_par_list(n,t,dic_all_t_comm):
    all_par_true=[]
    for i in range(t):
        par_true=[0]*n
        ite=[]
        flag=0
        for j in dic_all_t_comm[i]:
            ite.append((j,flag))
            flag+=1
        for u,v in ite:
            for j in u:
                par_true[int(j)-1]=v   #节点是从一记录的
        all_par_true.append(par_true)
    return all_par_true
    
def plot_NMI_all_t1(t,n,all_G,par_true):
    NMI=[]
    for i in range(t):
        G=all_G[i]
        node_partition = community_louvain.best_partition(G)
        comm_partition=LOUconvert2.LOUconvert(node_partition)
        par_list=[0]*n
        for j in range(n):
            par_list[j]=node_partition[j]
        
        NMI.append(metrics.normalized_mutual_info_score(par_list, par_true[i]))
    print(NMI)  
    '''
    plot the NMI for the initial data
    '''
    x=[i for i in range(t)]
    plt.plot(x,NMI,'-o',color='c',markerfacecolor='darkslategray',markeredgecolor='darkslategray')
    plt.xlabel('t',fontsize=14)
    plt.ylabel('NMI',fontsize=14)
    plt.grid(linestyle='--')
    x_major_locator=MultipleLocator(1)
    ax=plt.gca()
    ax.xaxis.set_major_locator(x_major_locator)
    plt.show()
    return  

def plot_NMI_all_t2(t,n,all_node_partition,par_true):
    NMI=[]
    for i in range(t):
        node_partition = all_node_partition[i]
        par_list=[0]*n
        for j in range(n):
            par_list[j]=node_partition[j]

        NMI.append(metrics.normalized_mutual_info_score(par_list, par_true))
    print(NMI)  
    '''
    plot the NMI for the initial data
    '''
    x=[i for i in range(t)]
    plt.plot(x,NMI,'-o',color='c',markerfacecolor='darkslategray',markeredgecolor='darkslategray')
    plt.xlabel('t',fontsize=14)
    plt.ylabel('NMI',fontsize=14)
    plt.grid(linestyle='--')
    x_major_locator=MultipleLocator(1)
    ax=plt.gca()
    ax.xaxis.set_major_locator(x_major_locator)
    plt.show()
    return  

def get_NMI(t,n,all_node_partition,par_true):
    NMI=[]
    for i in range(t):
        node_partition = all_node_partition[i]
        par_list=[0]*n
        for j in range(n):
            par_list[j]=node_partition[j]
        #print(par_list)
        #print(par_true)
        NMI.append(metrics.normalized_mutual_info_score(par_list, par_true[i]))
    return NMI
    
