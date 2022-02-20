# -*- coding: utf-8 -*-
"""
Created on Sat Feb 12 17:16:04 2022

@author: Duca
"""

import math
import database_obrada as db
import pandas as pd


class Point:
    
    def __init__(self, index, timestamp, x, y):
        self.x = x
        self.y = y
        self.timestamp = timestamp
        self.index = index
        
    def __sub__(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
    
    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ", timestamp: " + str(self.timestamp) + ")"

def generate_points(coordinates):
    list_of_points = []
    
    coordinates.reset_index()
    for index, row in coordinates.iterrows():
        list_of_points.append(Point(row["Unnamed: 0"], row["Eyetracker timestamp"], \
                                    row["Gaze point X"], row["Gaze point Y"]))
            
    return list_of_points
        

if __name__ == '__main__':
    stimuli, maeasurements = db.breakup_stimuli('11.csv')
    
    lista = generate_points(maeasurements[stimuli[0]])
    for element in lista:
        print(element)