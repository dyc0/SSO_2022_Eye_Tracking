# -*- coding: utf-8 -*-
"""
Created on Sun Feb 13 18:59:47 2022

@author: Duca
"""

from matplotlib import pyplot as plt
import statistics

import database_obrada as db
import points as pt
import graph as gh

def edge_stats(edge, depth):
    lengths = [ed.length for ed in edge.get_neighbour_edges(depth)]
    mean = statistics.mean(lengths)
    sd = statistics.stdev(lengths)
    
    return mean, sd


def imst(point_list, sample_size, offset, BD, ER, ESD = 1):
    saccades = set()
    
    for i in range(0, offset, len(point_list) - sample_size):        
        sample = point_list[i : i+sample_size]
        
        mst = gh.Graph()
        mst.primm(sample)
        
        potential_cutoffs = set()
        cutoffs = set()
        
        for edge in mst.edges:
            cutoff = True
            for node in edge.connections:
                if not node.check_branching_depth(edge, BD):
                    cutoff = False
                    break
            if cutoff:
                potential_cutoffs.add(edge)
                    
        for edge in potential_cutoffs:
            mean, sd = edge_stats(edge, BD)
            if edge.length/mean > ER and edge.length > mean + ESD:
                cutoffs.add(edge)
        
        for edge in cutoffs:
            for node in edge.connections:
                saccades.add(node.point.index)
            
    return saccades
    
if __name__ == '__main__':
    keys, vals = db.breakup_stimuli("11.csv")
    
    for name in keys:
        g = gh.Graph()
        lista = pt.generate_points(vals[name])
        saccades = imst(lista, 30, 5, 3, 1, 5)
        g.primm(lista)
        
        fignum = 0
        fig = plt.figure(fignum)
        ax = fig.add_subplot(111)
        path = name.translate({ord(t): None for t in '1234567890() '})
        img = plt.imread("pairs of animals/" + path + ".jpg")
        ax.imshow(img, extent=[0+448, 1024+448, 0+156, 768+156])
        for i in range(len(lista) - 1):
            coordinates_x = [lista[i].x, lista[i+1].x]
            coordinates_y = [lista[i].y, lista[i+1].y]
            ax.plot(coordinates_x, coordinates_y, color = 'gray')
        for point in lista:
            if point.index in saccades:
                ax.plot(point.x, point.y, 'ro')
            else:
                ax.plot(point.x, point.y, 'bo', markersize = 2)
        fig.canvas.draw()
        plt.show()
        
        print(name)
        for point in lista:
            if point.index in saccades:
                print(point.index)
        
        fignum+=1
        
            