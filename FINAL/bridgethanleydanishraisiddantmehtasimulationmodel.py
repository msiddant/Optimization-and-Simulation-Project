# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 19:21:05 2019

@author: shakiba
"""

from random import *
from statistics import mean 
import numpy as np
from math import inf as Infinity
 
Avg_IAT = 3.0				# Average Inter-Arrival Time 
Avg_ST = [9.0,14.0,9.0]			# Average Service Time 
k=3
Limit=10

Num_customers = 1000    # Number of customers to be simulated


Entered_System_Data = []   # Collect arrival times
Entered_System_Data.append(expovariate(1.0/Avg_IAT))
for i in range(1,Num_customers):
     Entered_System_Data.append(Entered_System_Data[i-1]+expovariate(1.0/Avg_IAT))

Arr_Time_Data=Entered_System_Data[1:].copy()


Patient_Diag_Data=[] #Diagnosis Data
for i in range(Num_customers):
     Patient_Diag_Data.append(randint(1,3))

Severity_Data=[] #Severity Data
for i in range(Num_customers):
     Severity_Data.append(randint(1,15))



# Output Variables

Service_Beg_T=[]
Service_Beg_T.append(Entered_System_Data[0])

Srvc_Time_Data=[]    # Collect service times
Srvc_Time_Data.append(expovariate(1.0/Avg_ST[Patient_Diag_Data[0]-1]))
del Patient_Diag_Data[0]
Dep_Time_Data = []   # Collect departure times
Dep_Time_Data.append(Service_Beg_T[0]+Srvc_Time_Data[0])
timeServerAvail=[] #the list of time each server becomes available
timeServerAvail.append(Dep_Time_Data[0]) 
for kk in range (1,k):
    timeServerAvail.append(0.0) #Time that server is available

def update_queue(Arr_Time_Data,timeServerAvail,Limit,queue_data):
    Q=0
    for i in Arr_Time_Data[0:Limit-1]:
        if i < min(timeServerAvail):
                Q+=1
        queue_data.append(Q)    
blocked=[]
queue_data=[]
while len(Arr_Time_Data)!=0:
    if Arr_Time_Data[0]>min(timeServerAvail):#Server idle
        Service_Beg_T.append(Arr_Time_Data[0])
        Srvc_Time_Data.append(expovariate(1.0/Avg_ST[Patient_Diag_Data[0]-1]))
        Dep_Time_Data.append(Service_Beg_T[-1]+Srvc_Time_Data[-1])
        timeServerAvail[np.argmin(timeServerAvail)]=Dep_Time_Data[-1]
        del Arr_Time_Data[0]
        del Patient_Diag_Data[0]
    else:
        if len(Arr_Time_Data)>Limit and Arr_Time_Data[Limit]<min(timeServerAvail):
            blocked.append(Entered_System_Data.index(Arr_Time_Data[Limit]))
            del Arr_Time_Data[Limit]
        update_queue(Arr_Time_Data,timeServerAvail,Limit,queue_data)
        Service_Beg_T.append(min(timeServerAvail))
        Srvc_Time_Data.append(expovariate(1.0/Avg_ST[Patient_Diag_Data[0]-1]))
        Dep_Time_Data.append(Service_Beg_T[-1]+Srvc_Time_Data[-1])
        timeServerAvail[np.argmin(timeServerAvail)]=Dep_Time_Data[-1]
        del Arr_Time_Data[0]
        del Patient_Diag_Data[0]
for i in blocked:
    Entered_System_Data[i]=Infinity

while Infinity in Entered_System_Data:
    Entered_System_Data.remove(Infinity)
    
Delay_Data=[]
for i in range(len(Entered_System_Data)):
    d=Service_Beg_T[i]-Entered_System_Data[i]
    if d>1e-6:
        Delay_Data.append(d)
    else:
        Delay_Data.append(0.0)
        
print("Average waiting time= ",round(mean(Delay_Data),4))
print("Total number of lost customers= ", len(blocked))
print("Server Utilization= ", round(sum(Srvc_Time_Data)/Dep_Time_Data[-1],4))
print("Average Number of Customers waiting= ", round(mean(queue_data),4))
print("Average Waiting Time= ", round(mean(Delay_Data),4))