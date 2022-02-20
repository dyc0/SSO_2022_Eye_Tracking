# -*- coding: utf-8 -*-
"""
Created on Sat Feb 12 13:23:29 2022

@author: Duca
"""

'''
Prva fja izvlaci sve podatke koji mogu da nam budu bitni u daljem radu, druga
razbija merenja po stimulusima.

Mozete da importujete ovaj fajl kao
#import database_obrada as db
i onda koristite ove fje direktno u svom kodu. Najbolje da ga sacuvate u istom
direktorijumu kao i svoj kod. Ako pokrenete kod direktno odavde
poziva se onaj deo u if __name__=='__main__', pa se izvrsava fja koja ekstrahuje
potrebne podatke, ali ne i ona koja ih razbija po stimulusima.
'''


# RAD SA TABELAMA

import pandas as pd
import os.path


def extract_basics():
    # Fja izvlaci nama potrebne podatke za obradu iz onih velikih tabela. Uklanjaju se
    # sva stanja koja su bila invalid, odseca se kalibracija i sklanjaju sva NaN stanja.
    # Ostaju kolone: Index, Eyetracker timestamp, Gaze point X, Gaze point Y i
    # Presented Stimulus name. Rezultati se ispisuju u tabele u istom direktorijumu
    # gde je kod.
    
    for i in range(1, 4):
        for j in range(1, 4):
            
            name = "Ispitanik " + str(i) + " redosled " + str(j) + ".xlsx"
            
            if not os.path.isfile(name):
                continue
            
            outname = str(i) + str(j) + ".csv"
    
            in_file = pd.read_excel(name)
            data = in_file[["Eyetracker timestamp", "Gaze point X", "Gaze point Y", \
                            "Presented Stimulus name", "Validity left"]]
            data = data[data["Validity left"] == "Valid"]
            data = data[data["Presented Stimulus name"] != "Eyetracker Calibration"]
            data = data[data["Presented Stimulus name"].notnull()]
            data = data.drop(labels="Validity left", axis = 1)
            
            data.to_csv(outname)


def breakup_stimuli(name):
    # Tabela se razbija na manje tabele, tako da svaki stimulus bude u zasebnoj.
    # Iskljucuju se delovi u kojima smo slusali zvuk, ostaju samo delovi sa slikama.
    # Ulaz je ime fajla u kome je isfiltrirana tabela preko fje extract_basics().
    # Izlaz je par (stimuli, measurements), gde je stimuli lista imena svih stimulusa,
    # a measurements recnik u kome je kluc ime stimulusa, a vrednost tabela sa merenjima
    # za taj stimulus.
    
    in_file = pd.read_csv(name)
    
    stimuli = in_file["Presented Stimulus name"].unique()
    stimuli = stimuli[1::2]
    measurements = {}
    
    for stimulus in stimuli:
        cur = in_file[in_file["Presented Stimulus name"] == stimulus]
        cur = cur.drop(labels = "Presented Stimulus name", axis = 1)
        measurements[stimulus] = cur
        
    return stimuli, measurements
        

if __name__ == '__main__':
    extract_basics()
    