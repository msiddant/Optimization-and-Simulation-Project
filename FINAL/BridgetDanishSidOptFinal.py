# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 01:07:55 2020

@author: danis
"""

from pyomo.environ import *
import pandas
import random

df=pandas.read_excel('C:\\Users\\bhanl004\\Downloads\\pythondata.xlsx','Diagnosis',header=0,index_col=0)
I=list(df.index.map(int))
J=[df.at[i,"Diagnosis"] for i in I]

df2=pandas.read_excel('C:\\Users\\bhanl004\\Downloads\\pythondata.xlsx','Severity',header=0,index_col=0)
Severity={(i,j):df2.at[i,j] for i in I for j in list(df2.columns.map(int))}


df3=pandas.read_excel('C:\\Users\\bhanl004\\Downloads\\pythondata.xlsx','Facility',header=0,index_col=0)
K=list(df3.index.map(int))
FType=[df3.at[k,"Facility Type"] for k in K]




##Generating and assigning random numbers for capacity
rcbeds1=[df3.at[k,"RCBEDS"] for k in K]

#rcbeds1=[]
#for k in K:
 #   if rcbeds[k-1] in [-1,-2]:
  #      rcbeds1.append(random.randint(1,1))        
   # else:
    #    rcbeds1.append(rcbeds[k-1])

Capacity=[]
for k in K:
    if rcbeds1[k-1] in [-1,-2]:
        Capacity.append(0)
    elif rcbeds1[k-1] == 1:
        Capacity.append(random.randint(1,10))
    elif rcbeds1[k-1] == 2:
        Capacity.append(random.randint(11,20))
    elif rcbeds1[k-1] == 3:
        Capacity.append(random.randint(21,30))
    elif rcbeds1[k-1] == 4:
        Capacity.append(random.randint(31,40))
    elif rcbeds1[k-1] == 5:
        Capacity.append(random.randint(41,50))
    elif rcbeds1[k-1] == 6:
        Capacity.append(random.randint(51,75))
    elif rcbeds1[k-1] == 7:
        Capacity.append(random.randint(76,100))
    elif rcbeds1[k-1] == 8:
        Capacity.append(random.randint(101,250))
    elif rcbeds1[k-1] == 9:
        Capacity.append(random.randint(251,260))


#Combining the two lists to create a dictionary

FacType={j:[] for j in J}
for key, value in zip(FType,K):
    FacType[key].append(value)


FacType[1]+=FacType[3]
FacType[2]+=FacType[3]

P=3

#Severity For Diagnosis of Patient i
S=[]
for i in I:
    S.append(Severity[i,J[i-1]])

model=ConcreteModel()

model.X=Var(I,K,within=Binary)


def obj_rule(m):
    return sum(1-sum(model.X[i,k] for k in FacType[J[i-1]])*P*S[i-1] for i in I) -sum(P*S[i-1]*model.X[i,k] for k in FacType[J[i-1]] for i in I)

model.obj=Objective(rule=obj_rule)

model.cap1=ConstraintList()
for k in K:
    model.cap1.add(sum(model.X[i,k] for i in I)<=Capacity[k-1])

model.cap2=ConstraintList()
for i in I:
    model.cap2.add(sum(model.X[i,k] for k in FacType[J[i-1]])<=1)


