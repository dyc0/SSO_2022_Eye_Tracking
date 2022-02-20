# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14 05:37:38 2022

@author: Duca
"""

import os
import pandas as pd

import data_processing as dp
import database_obrada as db
import graph as gh
import image_positions
import imst
import points as pt

def generate_results(results_table, stimuli_table):
    for ispitanik in range(1, 4):
        for order in range(1, 4):

            name = str(ispitanik) + str(order) + ".csv"
            if not os.path.isfile(name):
                continue

            keys, vals = db.breakup_stimuli(name)

            index = 1
            for image_name in keys:
                img_name = image_name.translate({ord(t): None for t in '1234567890() '})
                stimulus_name = stimuli_table.iloc[index-1, order-1]
                present = image_positions.eye_track(img_name, stimulus_name)

                point_list = pt.generate_points(vals[image_name])
                saccades = imst.imst(point_list, 30, 5, 3, 1, 5)
                g = gh.Graph()
                g.primm(point_list)
                cl = dp.Clusters(g, saccades)

                results = {"Stimulus": present,\
                           "Dispersion X": cl.mean_cluster_dispersion()[0],\
                           "Dispersion Y": cl.mean_cluster_dispersion()[1],\
                           "No. of Clusters": cl.get_number_of_clusters(),\
                           "No. of Saccades": cl.get_number_of_saccades()}

                results_table = results_table.append(results, ignore_index=True)

                index += 1

    return results_table


if __name__ == '__main__':
    column_names = ["Stimulus", "Dispersion X", "Dispersion Y", "No. of Clusters", "No. of Saccades"]
    results_table = pd.DataFrame(columns=column_names)
    stimuli_table = pd.read_excel("LookAt.xlsx")

    results_table = generate_results(results_table, stimuli_table)
    results_table.to_csv("Results.csv")
