# -*- coding: utf-8 -*-
'''
    input:
        f,beta,x,N,alpha
    output:
        abstain or(yhat,L)

'''
import sys
sys.path.append("./code/CERTIFY")
sys.path.append("./code/get_all_partition")
from scipy.stats import beta 
from scipy import stats
import numpy as np
import math
from get_all_t import get_partition    #讲矩阵转换为G数据结构并进行社区检测
sys.path.append("./code/util/NMI_com")
import for_NMI
from decimal import *
import matplotlib.pyplot as plt
#%%


class Certify:
    def __init__(self,x,n,t,gammasets,true_list,**arg):
        self.x=x                        #二进制图数据 矩阵形式   （bi_len*t）
        self.t=t                        #时间节点数
        self.n=n                        #图的结点数
        self.gammasets=gammasets
        self.beta=0.99               #噪声参数
        self.alpha=0.01               #假设检验参数
        self.N=10                #采样数
        self.bi_len=int(self.n*(self.n-1)/2)   #矩阵的行数
        self.attack_way=0 # 默认为split攻击
        self.allNMI_file_path='./code/NMI/'
        self.true_list=true_list
        self.attack_t=0     #攻击时刻，从0开始记
        if arg:
            for k,v in arg.items():
                setattr(self,k,v)
    def getNMI(self):
        return self.allNMI
    
        '''
    def __init__(self,x,n,t,beta,alpha,N,gamma,attack_way):
        self.x=x                        #二进制图数据 矩阵形式   （bi_len*t）
        self.t=t                        #时间节点数
        self.n=n                        #图的结点数
        self.beta=beta                  #噪声参数
        self.alpha=alpha                #假设检验参数
        self.N=N                        #采样数
        self.gamma=gamma                 #平滑参数
        self.bi_len=self.n*(self.n-1)/2   #矩阵的行数
        self.attack_way=attack_way # 默认为split攻击
        '''
       
    '''
    f function
    input:partition_all_t,gamma_Set(such as:{0: ['2', '1', '4'], 1: ['2', '1', '4'], 2: ['2', '1', '4'], 3: ['2', '1', '4']})
    return value 0 or 1
    '''
    def f(self,all_node_partition,gamma_set):
        end_flag=0
        flag=-1
        for key,value in gamma_set.items():
            node_partition=all_node_partition[key]
            flag=node_partition[int(value[0])]
            for node in value:
                if node_partition[int(node)]!=flag:
                    end_flag=1
                    break
            if end_flag==1:
                return 0
        return 1
    
    '''
        one_side clopper_person method
        input:alpha,top_number,N
        output:lower bound of confidence intervals
    '''
    def clopper_person(self,top_number):
       pl=stats.beta.interval(self.alpha,top_number+1,self.N-top_number+1)[0]
       pl=('%.4f'% pl)
       return float(pl)   
   
   
    '''
        input:
            beta:agrs
            x:original binary graph
            N:number for samples
            gamma_set 
            s or m:split or merge
            n:number of nodes for graph
        output:
           the top two answer
    
    '''       
    def sample_under_noise(self,gamma_set):    
        num={}
        num[0]=0
        num[1]=0
        
        for i in range(self.N):
            epsilon=np.random.rand(self.bi_len,self.t)
            epsilon[epsilon<self.beta]=0
            epsilon[epsilon>=self.beta]=1
            epsilon=epsilon.astype(int)
            
            sin_epsilon=np.zeros((self.bi_len,self.t))
            sin_epsilon=sin_epsilon.astype(int)
            sin_epsilon[:,self.attack_t]=epsilon[:,self.attack_t]
            
            dnumber=np.sum(sin_epsilon)
            withnoise=np.bitwise_xor(self.x,sin_epsilon)
            
            partition_all_t=get_partition(withnoise,self.n)
            #print(partition_all_t)
            NMI=for_NMI.get_NMI(self.t,self.n,partition_all_t,self.true_list)
            
            print("sample "+str(i)+':'+"noise number"+str(dnumber))
            print("NMI:"+str(NMI))
            with open(self.allNMI_file_path+'NMI'+str(self.beta)+'-'+str(self.attack_t)+'.txt','a') as fnmi:
                fnmi.write(str(dnumber))
                fnmi.write('\n')
                fnmi.write(str(NMI))
                fnmi.write('\n')
            
            out=self.f(partition_all_t,gamma_set)
            num[out]+=1
            
        '''
            if ''.join(out) in num.keys():
                num[''.join(out)]+=1
            else:
                num[''.join(out)]=1
        sorted(num.items(),key = lambda x:x[1],reverse = True) #降序排序
        first_2=[]
        count=0
        for key, value in dict.items():
           first_2.append((key, value))
           count+=1
           if count>=2:
               break
          '''
        return num
   
    '''
    permutation
    input: a,b,l:扰动上限
    '''
    '''
    def number_H(self,a,b,l):
        if (a+b-l)%2!=0:
            return 0
        elif a+b<l:
            return 0
        else:
            return math.comb(self.bi_len*self.t-l,(a+b-l)/2)*math.comb(l,(a-b+l)/2)
    '''

    def theta(self,e,i,l):
        if (e+l)%2!=0:
            return 0
        elif 2*i-e<l:
            return 0
        else:
            return math.comb(int(self.bi_len*self.t-l),int((2*i-e-l)/2))*math.comb(l,int((l-e)/2))
 
        

    '''
    修改，原来的是-n到n，要改成-矩阵大小到矩阵大小
    '''
    def com_pt_opti(self,l):
        pr_x_es={}
        pr_x_del_es={}
        for e in range(-self.bi_len*self.t,self.bi_len*self.t):
            e=int(e)
            if e%2==0:
                print('subspace'+str(e))
            pr_x_e=0
            pr_x_del_e=0
            for i in range(max(0,e),min(self.bi_len*self.t,self.bi_len*self.t+e)+1):
                pr_x_e+=pow(self.beta,self.bi_len*self.t-(i-e))*pow((1-self.beta),i-e)*self.theta(e, i, l)
                pr_x_del_e+=pow(self.beta,self.bi_len*self.t-i)*pow(1-self.beta,i)*self.theta(e, i, l)
            pr_x_es[e]=pr_x_e
            pr_x_del_es[e]=pr_x_del_e
        return pr_x_es,pr_x_del_es

    
    '''
    input:
        pl
    output:
        L
    '''
    def certifiedPerturbtionSize(self,pl):
        h_ratio={}        
        getcontext().prec=10
        for i in range(-self.bi_len*self.t,self.bi_len*self.t+1):
            #index begins from 1
            h_ratio[i+self.bi_len*self.t+1]=pow(Decimal(self.beta)/(1-Decimal(self.beta)),Decimal(i))
        h_ratio=dict(sorted(h_ratio.items(), key=lambda x: x[1], reverse=True))
        index_order=list(h_ratio.keys())
        '''
            l的枚举值,这里先设为20 ,从大往小枚举找
        '''
        L=-1
        for l in range(20)[::-1]:
            print('enumerate L:'+str(l))
            pr_x_es,pr_x_del_es=self.com_pt_opti(l)
            #get the value of mu
            pr_sum=0
            i=0
            while(pr_sum<pl):
                pr_sum+=pr_x_es[index_order[i]]
                i+=1
            mu=i-1
            pr_del=[]  #delta
            pr_ep=[]   #epsilon
            for i in range(1,mu):
                pr_del.append(pr_x_del_es[index_order[i-1]])
                pr_ep.append(pr_x_es[index_order[i-1]])
            '''
            直接取p的上界为0.5
            '''
            if sum(pr_del)+(pl-sum(pr_ep))*pr_x_del_es[index_order[mu-1]]/pr_x_es[index_order[mu-1]]>0.5:
                L=l
            else:
                continue
            return L

    
    '''
    main
    '''
    
    def apply_certify(self,gamma_set):
        num=self.sample_under_noise(gamma_set)
        if num[0]>num[1]:
            ans=0
            m_y=num[0]
        else:
            ans=1
            m_y=num[1]
        print('ans:'+str(ans)+'    '+'m_y:'+str(m_y))
        pl=self.clopper_person(m_y)
        '''
        直接取pB的上界为0.5
        '''
        if pl>0.5 and ans==1:
            L=-1
            pass
            L=self.certifiedPerturbtionSize(pl)
        else:
            L=-1
        print('get L:'+str(L))
        with open(self.allNMI_file_path+'ANS'+str(self.beta)+'-'+str(self.attack_t)+'.txt','a') as fn:
            fn.write(str(ans)+' '+str(m_y))
            fn.write('\n')
            fn.write(str(L))
            fn.write('\n')
        return ans,L
    '''
    for all gammasets
    '''
    def sets_certify(self):
        result=[]
        i=0
        print("---------beta:"+str(self.beta)+"----------")
        print("---------attack_t:"+str(self.attack_t)+"------")
        for gamma_set in self.gammasets:
            print('***gammaset:'+str(i))
            i+=1
            ans,L=self.apply_certify(gamma_set)
            if L!=-1:
                result.append((ans,L))
        with open(self.allNMI_file_path+'NMI'+str(self.beta)+'-'+str(self.attack_t)+'result'+'.txt','a') as fnmi:
            fnmi.write(result)
            fnmi.write('\n')
        return result
                


#%%