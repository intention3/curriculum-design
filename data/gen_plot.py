#coding=utf-8
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

def file_to_G(data_path,t_step,N):
    all_G=[]
    for t in range(1,t_step+1):
    #for t in range(1,2):
        G=nx.Graph()
        with open(data_path+"switch.t0"+"%d.comm" % t,"r") as f:
            nodes=list(range(N))
            #print(nodes)
            G.add_nodes_from(nodes)
            row=0  #社区编号从0开始
            comm_affli = np.zeros(N,dtype=int)
            for line in f:
                line=line.rstrip('\n')
                for s in line.split(' '):
                    if s!='':
                        num=int(s)
                        comm_affli[num-1]=row
                row+=1
        with open(data_path+"switch.t0"+"%d.edges" % t,"r") as f2:
            for line in f2:
                line=line.rstrip('\n')
                s=line.split(' ')
                G.add_edge(int(s[0])-1,int(s[1])-1)
        
        plot_graph_with_comm(G, comm_affli)
        all_G.append(G)
    return all_G

def plot_graph_with_comm(G,comm_affli):
    plt.figure()
    colors = ["#FFB6C1","#ADD8E6","#D8BFD8", "#DDA0DD","#90EE90","#20B2AA","#778899"
              ,"#FFFFE0","#E0FFFF"]
    pos = nx.spring_layout(G,k=0.3)
    for comm in range(np.max(comm_affli)+1):
        nodes=nx.draw_networkx_nodes(G, pos, nodelist=np.where(comm_affli==comm)[0].tolist(),
                               node_color=colors[comm],node_size=43,linewidths = 0.1)
        nodes.set_edgecolor("#000000") 
    nx.draw_networkx_edges(G, pos,width=0.6,alpha=0.3)
    plt.show()
    

#%%
line="1 2"
s=line.split(' ')
print(s)