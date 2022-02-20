# -*- coding: utf-8 -*-
"""
Created on Wed Feb 16 19:09:26 2022

@author: Minja
"""
import pandas as pd
import numpy as np

# Odredjuje da li je stimulus na prezentovanoj slici i sa koje strane se nalazi
def eye_track(picture, stimulus):
    list_split = picture.split('&')
    left = list_split[0]
    right = list_split[1].split('.')[0]
    if left == stimulus:
        return 'left'
    elif right == stimulus:
        return 'right'
    else:
        return 'None'
  
# Nalazi vremena kad su se ispitaniku pojavile slike
def times(in_file):
    in_file = in_file.drop_duplicates(subset = ["Presented Stimulus name"])
    in_file = in_file[1::2]
    time = in_file.iloc[:,1]
    return time
    
# Vremenski trenutak pojavljivanja prve fiksacije nakon prikazivanja slike
def first_time_pic(eye_track_list,timestamp,result):
    first_time_pic_list = []
    index_list = []
    indeks = 0
    if len(result[0]) != 1:
        for i in range(0,len(eye_track_list)):
            if(eye_track_list[i] != 'None'):
                indeks = first(timestamp[i],eye_track_list[i],result,indeks)
                first_time_pic_list.append(result[2][indeks])
    else:
        first_time_pic_list.append(result[2])
    return first_time_pic_list

# Nalazi indeks prvog elementa koji ispunjava uslove       
def first(vreme, strana, rez, indeks):
    for i in range(indeks,len(rez[0])):
        if vreme <= rez[2][i]:
            if strana == 'left':
                if rez[0][i] < 960: # 960px je sredina slike, ne pocinje od 0, ima ofset
                    return i
            elif strana == 'right':
                if rez[0][i] > 960:
                    return i
    