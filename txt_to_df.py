# -*- coding: utf-8 -*-
"""
Created on Sun Jul  4 23:04:45 2021

@author: Emma
"""

import pandas as pd
import os
import re

#Here you choose the folder with the txt.files you want to merge into an excel file 
directory = r"C:/Users/Emma/Documents/Uni/Thesis/Data dance"

def clean_data(original_df):
    # split up all elements in df into [variable, value] and collect data in a list
    data_list=[]
    for index,row in original_df.iterrows():
        boolean=row.str.contains(":").sum()
        if boolean>0: row = row.str.split(pat=":")
        data_list.append(row.item())

    print("A session has been added with "+str(len(data_list))+" elements in the list containing data from ",end="")

    # remove all tabs and whitespaces from the data
    regex = re.compile(r'[\t\s]')
    for e in range(len(data_list)):
        if type(data_list[e])==list:
            data_list[e][0]=regex.sub("",data_list[e][0])
            data_list[e][1]=regex.sub("",data_list[e][1])
        else:
            data_list[e]=regex.sub("",data_list[e])
    
    return data_list
    
def get_logframe_indices(my_list):
# create a list with the starting and ending indices of each logframe
    indices=[]
    
    for row in range(len(my_list)):
        if my_list[row] == '***LogFrameStart***' or my_list[row] == '***LogFrameEnd***':
            indices.append(row)
    
    return indices

def get_data (initial_df):
    
    #the other two functions are called to clean the data first and get the indices where each logframe starts and ends
    part_list=clean_data(initial_df)
    indices=get_logframe_indices(part_list)
    
    function_columns=["subject","session","procedure","sub trial number","feedback.ACC","feedback.CRESP","feedback.RESP","feedback.RT","h","cue.OnsetTime","cue.OnsetDelay"]
    file_df=pd.DataFrame(columns=function_columns)
    
    #subject and session is only assigned once per file
    for row in range(len(part_list)):
        if part_list[row][0] == 'Subject': subject=int(part_list[row][1]);print("subject "+str(subject)+".")
        elif part_list[row][0] == 'Session': session=int(part_list[row][1]);break
    
    #loop over starting indices of LogFrames
    for i in range(0, len(indices), 2):
        #only loop over lines within a LogFrame
        for e in range(indices[i]+1,indices[i+1]):
            if part_list[e][0]=='sequentie' or part_list[e][0]=='Experiment': flag=False; break #Level 1 and 5 from text file are excluded
            elif part_list[e][0] == 'Procedure': 
                flag=True 
                procedure=part_list[e][1]
                (feedbackACC,feedbackCRESP,feedbackRESP,feedbackRT,h,cueOnsetTime,cueOnsetDelay)= tuple(["X"]*7)
                if part_list[e][1] == 'cueprocedure' or part_list[e][1] == 'responsprocedure':
                    count+=1 #count the sub trial number
                else:
                    count=0
            elif part_list[e][0] == 'feedback.ACC': feedbackACC=float(part_list[e][1])
            elif part_list[e][0] == 'feedback.CRESP': feedbackCRESP=part_list[e][1]
            elif part_list[e][0] == 'feedback.RESP': feedbackRESP=part_list[e][1]
            elif part_list[e][0] == 'feedback.RT': feedbackRT=float(part_list[e][1])
            elif part_list[e][0] == 'h': h=int(part_list[e][1])
            elif part_list[e][0] == 'cue.OnsetTime': cueOnsetTime=float(part_list[e][1])
            elif part_list[e][0] == 'cue.OnsetDelay': cueOnsetDelay=float(part_list[e][1])
        if flag:
            data_dict={"subject":subject,"session":session,"procedure":procedure,"sub trial number":count, "feedback.ACC":feedbackACC,"feedback.CRESP":feedbackCRESP,"feedback.RESP":feedbackRESP,"feedback.RT":feedbackRT,"h":h,"cue.OnsetTime":cueOnsetTime,"cue.OnsetDelay":cueOnsetDelay}
            file_df=file_df.append(data_dict, ignore_index=True) #data from each LogFrame will be added as a row to the df of the file
        
    
    #final dataframe of one file is returned
    return file_df

final_df=pd.DataFrame()

#loop over all files in directory
for path in os.listdir(directory):
    path_complete = directory + '/' + path
    #Create initial dataframe
    df_base = pd.read_csv(path_complete, encoding='utf-16')
    #final dataframe of one file will be returned by the function get_data()...
    temp_df=get_data(df_base)
    #...and will be added to the overall dataframe
    final_df=final_df.append(temp_df)
        
#Save the file
final_df.to_excel(r"df_P23678.xlsx",index= False)