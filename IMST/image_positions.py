# -*- coding: utf-8 -*-
"""
Created on Wed Feb 16 19:09:26 2022

@author: Minja
"""

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
    
