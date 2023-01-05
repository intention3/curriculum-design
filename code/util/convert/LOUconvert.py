# -*- coding: utf-8 -*-
import numpy as np

def convert(f,index_max,dic,pos):
    comm_index=[]
    dicnew={}
    for i in range(index_max+1):      
        line=f.readline()
        if line:
            line=line.rstrip('\n')
            s=line.split(' ')
            for node in dic[int(s[0])]:
                if int(s[1]) not in dicnew:
                    dicnew[int(s[1])]=[]
                dicnew[int(s[1])].append(node)
            comm_index.append(int(s[1]))   
        else:
            print("read error")
            break
    if f.tell()!=pos:
        index_max=max(comm_index)
        dicnew=convert(f,index_max,dicnew,pos)
    return dicnew
        
def LOUconvert(N,filename):
    with open(filename,"r") as f:
        pos=f.seek(0,2)
    dic={}
    comm_index=[]
        
    with open(filename,"r") as f:
        for i in range(N):
            line=f.readline()
            if line:
                line=line.rstrip('\n')
                s=line.split(' ')
                if int(s[1]) not in dic:
                    dic[int(s[1])]=[]
                dic[int(s[1])].append(int(s[0]))
                comm_index.append(int(s[1]))   
            else:
                print("1:read error")
                break
        if f.tell()!=pos:
            index_max=max(comm_index)
            answer=convert(f,index_max,dic,pos)
        else:
            answer=dic
    return answer
        
        
            
#%%      
answer=LOUconvert(100,"code/util/graph.tree")  
 
#%%
print(pos)
