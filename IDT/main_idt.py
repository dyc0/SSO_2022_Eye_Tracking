# -*- coding: utf-8 -*-
"""
Created on Tue Feb 15 18:57:34 2022

@author: Minja
"""

import pandas as pd
import csv
import os
import numpy as np
import math
from idt import idt
import database_obrada as db
from eye_track import eye_track
from eye_track import times
from eye_track import first_time_pic
import statistics

data = []
  
root = "C:/Users/Minja/Desktop/ETF/3. godina/peti semestar/sso/projekat/nova_verzija/"

for i in range(1,4):
    for j in range(1,4):
        name = root + str(i) + str(j) + ".csv"
        if os.path.exists(name):
            # Citanje iz csv fajla, pri cemu je prethodno pokrenut program database_obrada.py
            sub_data = pd.read_csv(name)
            data.append(sub_data)
        else:
            continue
        
dis_tres = 40 #u pikselima
dur_tres = 100000 #100ms
rezultati = []
rez = []

for i in range(0,6):
    cX, cY, t0, t1, gaze_point_cnt, fix_dur = idt(data[i],dis_tres,dur_tres)
    rez.append(cX)
    rez.append(cY)
    rez.append(t0)
    rez.append(t1)
    rez.append(gaze_point_cnt)
    rez.append(fix_dur)
    rez_copy = rez.copy()
    rezultati.append(rez_copy)
    rez.clear()
    
# Broj klastera, tj. broj fiksacija
br_klastera = []
gaze_pcnt_mean = []
for i in range(0,6):
    br_klastera.append(len(rezultati[i][0]))
    gaze_pcnt = statistics.mean(rezultati[i][4])
    gaze_pcnt_mean.append(gaze_pcnt)
    

# Slike
pictures_list = ['bear&donkey.jpg','bison&camel.jpg', 'cow&rabbit.jpg','deer&frog.jpg',
                  'dog&elephant.jpg','giraffe&hedgehog.jpg','horse&monkey.jpg',
                  'kangoroo&rhinoceros.jpg','lion&pig.jpg','mouse&goat.jpg']

 
look_at_file = pd.read_excel('LookAt.xlsx')

# Sadrze informaciju da li se stimulus nalazi na slici i gde je
list_eye_track1 = []
list_eye_track2 = []
list_eye_track3 = []
for i in range(0,10):
    l = eye_track(pictures_list[i],look_at_file.iloc[i,0])
    list_eye_track1.append(l)
    l1 = eye_track(pictures_list[i],look_at_file.iloc[i,1])
    list_eye_track2.append(l1)
    l2 = eye_track(pictures_list[i],look_at_file.iloc[i,2])
    list_eye_track3.append(l2)
    
list_eye_track = [list_eye_track1, list_eye_track2, list_eye_track2, list_eye_track3,
                  list_eye_track1, list_eye_track3]

# Trazi vreme pojavljivanja slika ispitaniku
vreme_pojavljivanja_sl = []
vps_list = []
for i in range(0,6):
    vr = times(data[i])
    vreme_pojavljivanja_sl.append(vr)
# Prebacivanje u listu   
for i in range(0,6):
    vr = vreme_pojavljivanja_sl[i].values.tolist()
    vps_list.append(vr)
 
# Trazi se vreme prve fiksacije nakon prikazivanja svake slike
vremena_prve_fix = []
index_list = []
for i in range(0,6):
     pfirst = first_time_pic(list_eye_track[i], vps_list[i], rezultati[i])
     vremena_prve_fix.append(pfirst)

# Trazi razliku, odnosno vreme koje prodje do pocetka prve fiksacije nakon prikaza
# prve slike u eksperimentu     
eye_track_niz = np.array(list_eye_track) #prebacivanje u niz
niz = eye_track_niz != 'None' #elementi koji su 'None' imaju vrednost false
indeksi = (niz!=0).argmax(axis=1) #trazi indekse prvih elemenata u svakoj vrsti koji
                                #su razliciti od false
razlike = []
for i in range(0,len(vremena_prve_fix)):
    raz = vremena_prve_fix[i][0] - vps_list[i][indeksi[i]]
    razlike.append(raz)

