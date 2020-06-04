# -*- coding: utf-8 -*-
"""
Created on Thu May 05 21:25:17 2020

@author: danis
"""

from random import *
from statistics import mean 
import numpy as np
from math import inf as Infinity
 
Avg_IAT = 0.25				# Average Inter-Arrival Time Patients arrive Every 6 hours on avg. (24 hrs*.25)
Avg_ST = [25.0,50.0,75.0]		# Average Service Time  (Mental Health 25 days, Substance Abuse 50 days, Both: 75 Days)
k=125                               #No of beds avialable
Limit=8                             #Limit of five patients waiting in the queue

Num_customers = 1000                # Number of patients to be simulated

# Collect arrival times
Entered_System_Data = []   
Entered_System_Data.append(expovariate(1.0/Avg_IAT))
for i in range(1,Num_customers):
     Entered_System_Data.append(Entered_System_Data[i-1]+expovariate(1.0/Avg_IAT))

Arr_Time_Data=Entered_System_Data[1:].copy()


# Collect patient diagnosis data
Patient_Diag_Data=[] #Diagnosis Data
for i in range(Num_customers):
     Patient_Diag_Data.append(randint(1,3))

#Severity Data
Severity_Data=[] #Severity Data
for i in range(Num_customers):
     Severity_Data.append(randint(1,15))



# Output Variables
Service_Beg_T=[]
Service_Beg_T.append(Entered_System_Data[0])

#Collect service times for first patient
Srvc_Time_Data=[]    
Srvc_Time_Data.append(expovariate(1.0/Avg_ST[Patient_Diag_Data[0]-1]))
del Patient_Diag_Data[0]
del Severity_Data[0]

#Collect Departure and time Server is available 
Dep_Time_Data = []   # Collect departure times
Dep_Time_Data.append(Service_Beg_T[0]+Srvc_Time_Data[0])

#the list of time each server becomes available
timeServerAvail=[] 
timeServerAvail.append(Dep_Time_Data[0]) 
for kk in range (1,k):
    timeServerAvail.append(0.0) #Time that server is available

#Function to keep track of the queue data
def update_queue(Arr_Time_Data,timeServerAvail,Limit,queue_data):
    Q=0
    for i in Arr_Time_Data:
        if i < min(timeServerAvail) and Q<Limit:
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
        del Severity_Data[0]
    else:
        if len(Arr_Time_Data)>Limit and Arr_Time_Data[Limit]<min(timeServerAvail):#All Servers busy
            blocked.append(Entered_System_Data.index(Arr_Time_Data[Limit]))
            del Arr_Time_Data[Limit]
            del Patient_Diag_Data[Limit]
            del Severity_Data[Limit]
        update_queue(Arr_Time_Data,timeServerAvail,Limit,queue_data)
        Service_Beg_T.append(min(timeServerAvail))
        Srvc_Time_Data.append(expovariate(1.0/Avg_ST[Patient_Diag_Data[np.argmax(Severity_Data[0:Limit])]-1]))
        Dep_Time_Data.append(Service_Beg_T[-1]+Srvc_Time_Data[-1])
        timeServerAvail[np.argmin(timeServerAvail)]=Dep_Time_Data[-1]
        del Arr_Time_Data[np.argmax(Severity_Data[0:Limit])]
        del Patient_Diag_Data[np.argmax(Severity_Data[0:Limit])]
        del Severity_Data[np.argmax(Severity_Data[0:Limit])]

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
        
Time_System=[]
for i in range(len(Dep_Time_Data)):
    b= Dep_Time_Data[i] - Entered_System_Data[i]
    if b>1e-6:
        Time_System.append(b)
    else:
        Time_System.append(0.0)

        
#Performance Matrix
print("Average waiting time (Days)= ",round(mean(Delay_Data),4))
print("Average Service time (Days)= ", round(mean(Srvc_Time_Data),4))
print("Average Time in the System (Days)= ", round(mean(Time_System),4))
print("Portion of Lost Patients = ", round(len(blocked)/Num_customers,4))
print("Average Server Utilization= ", round(sum(Srvc_Time_Data)/(k*Dep_Time_Data[-1]),4))
print("Average Number of Customers waiting= ", round(mean(queue_data),4))
