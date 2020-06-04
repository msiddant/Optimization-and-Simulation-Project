# -*- coding: utf-8 -*-
"""
The arrival process is a Poisson process with an average inter-arrival time of
 2.0 (line 19). 
 The departure process is also a Poisson process with an average 
 service time of 1.0 (line 20). 
 The system will be simulated for 100.0 time units (line 21). 
 
The simulation clock is initialized to zero and it is used  to keep track of 
the simulation time (line 22).


"""

from random import *
from math import inf as Infinity
from statistics import mean

Avg_IAT = 10.0                # Average Inter-Arrival Time 
Avg_ST1 = 4.0
Avg_ST2 = 7.0
Avg_ST3 =5.0                 # Average Service Time 
Tot_Sim_Time = 10.0        # Total Simulation Time 
clock = 0.0                 # Current Simulation Time
departureCount=0.0          #Starting Departure Count                
Num_Customer=1000
N = 0    # State variable; number of customers in the system


Arr_Time_Data=[]
Service_Time_Data=[]
Departure_Time_Data=[]
Delay=[]
Time_In_System_Data=[]
Patient_Diag_Data=[]
# Time of the next arrival event
Arr_Time = expovariate(1.0/Avg_IAT)

arrivalCount=1
print("customer",arrivalCount," arrives at ",Arr_Time)

# Time of the next departure event
Dep_Time = Infinity
departureCount=0                    

while departureCount < Num_Customer:
    if Arr_Time < Dep_Time:# Arrival Event
         clock = Arr_Time
         Arr_Time_Data.append(Arr_Time)
         Patient_Diag_Data.append(randint(1,3))
         N = N + 1.0
         if N == 1:
             if Patient_Diag_Data[-1]==1:
                 Service_Time_Data.append(expovariate(1.0/Avg_ST1))
                 Dep_Time = clock + Service_Time_Data[-1]
             if Patient_Diag_Data[-1]==2:
                 Service_Time_Data.append(expovariate(1.0/Avg_ST2))
                 Dep_Time = clock + Service_Time_Data[-1]
             if Patient_Diag_Data[-1]==3:
                 Service_Time_Data.append(expovariate(1.0/Avg_ST3))
                 Dep_Time = clock + Service_Time_Data[-1]
         Arr_Time = clock + expovariate(1.0/Avg_IAT)
         arrivalCount+=1
    else: # Departure Event
         clock = Dep_Time 
         Departure_Time_Data.append(Dep_Time)
         N = N - 1.0
         departureCount+=1
         if N > 0:
             if Patient_Diag_Data[departureCount-1]==1:
                 Service_Time_Data.append(expovariate(1.0/Avg_ST1))
                 Dep_Time = clock + Service_Time_Data[-1]
             if Patient_Diag_Data[departureCount-1]==2:
                 Service_Time_Data.append(expovariate(1.0/Avg_ST2))
                 Dep_Time = clock + Service_Time_Data[-1]
             if Patient_Diag_Data[departureCount-1]==3:
                 Service_Time_Data.append(expovariate(1.0/Avg_ST3))
                 Dep_Time = clock + Service_Time_Data[-1]
         else:
             Dep_Time = Infinity
NumWaiting=0
threshold=3.0
NumWaitingLongerthan=0
for i in range(Num_Customer):
    Time_In_System_Data.append(Departure_Time_Data[i]-Arr_Time_Data[i])   
    d=Departure_Time_Data[i]-Arr_Time_Data[i]-Service_Time_Data[i]
    if  d>1e-6:
        Delay.append(d)
        NumWaiting+=1
        if d>threshold:
            NumWaitingLongerthan+=1
    else:
        Delay.append(0.0)
    
           
print("Average Wait Time = ",round(mean(Delay),4))
print("Average Time In System = ",round(mean(Time_In_System_Data),4))
print("Probability of Waiting =",(NumWaiting/Num_Customer))
print("Probability of Waiting Longer than",threshold,"= ",(NumWaitingLongerthan/Num_Customer))
print("Utilization Time= ",round((sum(Service_Time_Data)/Departure_Time_Data[-1]),4))
print("Maximum Waiting Time= ",max(Delay))