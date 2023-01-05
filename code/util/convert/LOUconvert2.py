# -*- coding: utf-8 -*-

def LOUconvert(partition):
    num=max(partition.values())+1
    dic={}
    for i in range(num):
        dic[i]=[]
    for key,value in partition.items():
        dic[value].append(key)
    return dic