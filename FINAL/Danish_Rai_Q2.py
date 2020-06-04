# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 20:43:35 2019

@author: shakiba
"""



from random import expovariate
from math import inf as Infinity
from statistics import mean 
import numpy as np


 
Avg_IAT = 5.0				# Average Inter-Arrival Time 
Avg_ST = 20.0 				# Average Service Time 
k=5 #Number of servers

RenegT=10.0

StoppingCondition=8*60    # Time that simulation will be over


# Output Variables

Arr_Time_Data = []   # Collect arrival times

Service_Beg_T=[] # Collect Service Start times


Srvc_Time_Data=[]    # Collect service times


Dep_Time_Data = []   # Collect departure times


timeServerAvail=[0.0 for kk in range (k)] #the list of time each server becomes available

N=0    #Number of cutomers arriving
renegList=[]
clock=0
while clock<StoppingCondition:#MISSING CODE: #Is it clock? #Review
    if N>0:#MISSING CODE:
        N+=1
        Arr_Time_Data.append(Arr_Time_Data[-1]+expovariate(1.0/Avg_IAT))
    else:
        N+=1
        Arr_Time_Data.append(expovariate(1.0/Avg_IAT))
    if Arr_Time_Data[-1]>min(timeServerAvail):#MISSING CODE  #at least one server is  idle
        Service_Beg_T.append(Arr_Time_Data[-1])#MISSING a segment of code
        Srvc_Time_Data.append(expovariate(1/Avg_ST))
        Dep_Time_Data.append(Service_Beg_T[-1]+Srvc_Time_Data[-1])
        timeServerAvail[np.argmin(timeServerAvail)]=Dep_Time_Data[-1]
        clock=Dep_Time_Data[-1]#MISSING A FEW LINES OF CODE
    else:#all servers are busy #reneg
        if min(timeServerAvail) - Arr_Time_Data[-1]<RenegT:
            Service_Beg_T.append(min(timeServerAvail))#MISSING a segment of code
            Srvc_Time_Data.append(expovariate(1/Avg_ST))
            Dep_Time_Data.append(Service_Beg_T[-1]+Srvc_Time_Data[-1])
            timeServerAvail[np.argmin(timeServerAvail)]=Dep_Time_Data[-1]
            clock=Dep_Time_Data[-1]
        else:
            renegList.append(N-1) # Index of the person who left #MISSING A FEW LINES OF CODE

#Removing Reneged Customers
for i in renegList:
    Arr_Time_Data[i]=Infinity

while Infinity in Arr_Time_Data:
    Arr_Time_Data.remove(Infinity)


Delay_data=[]
for i in range(len(Service_Beg_T)):
    d= Service_Beg_T[i] - Arr_Time_Data[i]
    if d>0.0000000000001:
        Delay_data.append(d)
    else:
        Delay_data.append(0.0)   
        
Time_System=[]
for i in range(len(Dep_Time_Data)):
    d= Dep_Time_Data[i] - Arr_Time_Data[i]
    if d>0.0000000000001:
        Time_System.append(d)
    else:
        Time_System.append(0.0)  
    
    
#Server avail at 9:30
#Customer comes at 9:15
#Server avial - arrival =15
#wait is 15 which is longer than the Reneg time        
###################################################################################        
#Collect Performance Measures

#proportion of reneged customers
print("Proportion of Renenged Customers= ", len(renegList)/N)
#average server utilization assuming all servers have the same workload,
print("Average Server Utlization= ",round(sum(Srvc_Time_Data)/Dep_Time_Data[-1],4))
#average waiting timefor customers who stay in the bank,
print("Average Waiting Time= ", round(mean(Delay_data),4))
#verage time spent in the system for customers who stay in the bank
print("Average Time in the System= ", round(mean(Time_System),4))
