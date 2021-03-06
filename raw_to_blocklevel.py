# -*- coding: utf-8 -*-
"""
Created on Mon Jul  5 00:21:48 2021

@author: Emma
"""


import pandas as pd

df = pd.read_excel (r"C:/Users/Emma/Documents/Uni/Thesis/Code and df dance/df_P23678.xlsx")


#arrange data on trial level: average RT and overall accuracy

block_columns=["subject","session","trial","sub_trial","accuracy","RT","h"]
df_block=pd.DataFrame(columns=block_columns)
subjects=[]

for index,row in df.iterrows():
    if row["subject"] not in subjects:
        trial=0    #counts sequences over whole experiment
        sub_trial=0    # counts sequences within one session
        subjects.append(row["subject"])
        sessions=[row["session"]]
    if row["procedure"]=="responsprocedure":
        if row["sub trial number"]==1:
            trial+=1
            RT = float(row["feedback.RT"])
            accuracy = int(row["feedback.ACC"])
            if row["session"] in sessions:
                sub_trial+=1
            else:
                sub_trial=1
                sessions.append(row["session"])
        elif row["sub trial number"]==6:
            RT += float(row["feedback.RT"])
            accuracy += int(row["feedback.ACC"])
            RT = RT / 6
            if accuracy==6: accuracy=1
            else: accuracy=0
            data_dict={"subject":row["subject"],"session":row["session"],"trial":trial,"sub_trial":sub_trial,"accuracy":accuracy,"RT":RT/1000,"h":row["h"]}
            df_block=df_block.append(data_dict, ignore_index=True)
        else:
            RT += float(row["feedback.RT"])
            accuracy += int(row["feedback.ACC"])
            
#create counts for how many times one specific sequence was practiced
subjects=[]
list_h=[]
repetitions=[]

for index, row in df_block.iterrows():
    if row["subject"] not in subjects:
        list_h=[]
        subjects.append(row["subject"])
    if list_h==[]: 
        a=row["h"]
        list_h.append(a)
        a_count=0
        repetitions.append(a_count)
    elif row["h"] not in list_h: 
        b=row["h"]
        list_h.append(b)
        b_count=0
        repetitions.append(b_count)
    elif row["h"]==a: a_count+=1; repetitions.append(a_count)
    else: b_count+=1; repetitions.append(b_count)
df_block["repetition"]=repetitions

#create new column to plot learning curves per subject per sequence

subject=[]
combi_count=-1
combi=[]

for i,r in df_block.iterrows():
    if r["subject"]not in subject: 
        subject.append(r["subject"])
        combi_count+=2
    if r["h"]==1:
        combi.append(combi_count)
    else:
        combi.append(combi_count+1)

df_block["subject_h"]=combi

subjects=[]
for i,r in df_block.iterrows():
    if r["subject"]==2:
        subjects.append(1)
    elif r["subject"]==3:
        subjects.append(2)
    elif r["subject"]==6:
        subjects.append(3)
    elif r["subject"]==7:
        subjects.append(4)
    elif r["subject"]==8:
        subjects.append(5)
df_block["subject"]=subjects

df_block.to_excel(r"C:/Users/Emma/Documents/Uni/Thesis/Code and df dance/df_triallevel_23678.xlsx",index= False)