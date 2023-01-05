# -*- coding: utf-8 -*-
import random
import operator


#%%
def get_grount_truth_comm(t,true_comm_path):
    dic_all_t_comm={}
    for i in range(t):
        dic_all_t_comm[i]=[]
        with open(true_comm_path+'switch.t0%d.comm' %(i+1)) as f:
            while(True):
                line=f.readline()
                if line:
                    community=[]
                    line=line.rstrip('\n')
                    ns=line.split()
                    for n in ns:
                        community.append(n)
                    dic_all_t_comm[i].append(community)
                else:
                    break
    #print(dic_all_t_comm)
    return dic_all_t_comm
def get_timeline_inf(timeline_path,dic_all_t_comm):
    tracker={}
    rel_judge=[]
    i=-1
    with open(timeline_path+'switch.timeline') as f:
        while(True):
            i+=1
            line=f.readline()
            if line:
                line=line.rstrip('\n')
                dc=line.split(':')[1]
                ns=dc.split(',')
                tracker[i]={}
                for n in ns:
                    s=n.split('=')
                    t=int(s[0])
                    row=int(s[1])
                    tracker[i][t-1]=dic_all_t_comm[t-1][row-1]
            else:
                
                break
    
    for key,value in tracker.items():
        judge=[]
        length=len(list(value.values())[0])
        for comm in list(value.values()):
            #print(comm)
            if len(comm)==length:
                judge.append(1)
            elif len(comm)>length:
                judge.append(2)
            else:
                judge.append(3)
            length=len(comm)
        rel_judge.append(judge)
    #print("动态社区追踪")
    #print(tracker)  
    #print("和前一个社区的判断")
    #print(rel_judge)         
    return tracker,rel_judge

def get_gammaset(t,tracker,rel_judge,gamma):
    gammasets=[]
    iflag=0
    for key,value in tracker.items():
        if len(list(value.values())[0])>gamma:
            for i in range(2):
                null=0
                gamma_split={}
                gamma_split[list(value.keys())[0]]=[]
                keys=random.sample(range(0,len(list(value.values())[0])),gamma)
                for keyi in keys:
                    gamma_split[list(value.keys())[0]].append(int(list(value.values())[0][keyi])-1)
                for showtimes in range(1,len(rel_judge[iflag])):
                    if rel_judge[iflag][showtimes]==1:
                        gamma_split[list(value.keys())[showtimes]]=gamma_split[list(value.keys())[showtimes-1]]
                    elif rel_judge[iflag][showtimes]==2:  #bigger
                        keys=random.sample(range(0,len(list(value.values())[showtimes])),gamma)
                        gamma_split[list(value.keys())[showtimes]]=[]
                        for keyi in keys:
                            gamma_split[list(value.keys())[showtimes]].append(int(list(value.values())[showtimes][keyi])-1) 
                    else:
                        union=list(set(gamma_split[list(value.keys())[showtimes-1]]) & set(list(value.values())[showtimes]))
                        if union:
                            gamma_split[list(value.keys())[showtimes]]=[u-1 for u in int(union)]
                        else:
                            #print("null")
                            null=1
                            break
                if null!=1:
                    gammasets.append(gamma_split)
                                             
        iflag+=1             
    print(gammasets)  
    return gammasets
'''
true_comm_path='E:/18.科研/robust/dycoding/data/data/sample/'
timeline_path='E:/18.科研/robust/dycoding/data/data/sample/'
dic_all_t_comm=get_grount_truth_comm(4, true_comm_path)
tracker,rel_judge=get_timeline_inf(timeline_path,dic_all_t_comm)
get_gammaset(4,tracker,rel_judge,3)
'''



