# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14 05:37:38 2022

@author: Duca
"""

import copy
from matplotlib import pyplot as plt
import statistics as st

import database_obrada as db
import points as pt
import graph as gh
import imst


class Cluster:

    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges

    def get_cluster_dispersion(self):
        if len(self.nodes) < 2:
            return [0, 0]
        xs = [node.point.x for node in self.nodes]
        ys = [node.point.y for node in self.nodes]

        return [st.stdev(xs), st.stdev(ys)]

    def get_cluster_means(self):
        xs = [node.point.x for node in self.nodes]
        ys = [node.point.y for node in self.nodes]
        return st.mean(xs), st.mean(ys)



class Clusters:

    def __init__(self, eyegaze_graph, saccades):
        self.clusters = []
        self.g = copy.deepcopy(eyegaze_graph)
        self.g.get_nodes_ordered()
        self.saccades = saccades

        self.remove_saccades()
        self.generate_clusters()
        return

    def remove_saccades(self):
        for index in self.saccades:
            for node in self.g.nodes:
                if node.point.index == index:
                    self.g.remove_node(node)

    def generate_clusters(self):
        reached_nodes = set()

        for node in self.g.nodes:
            if node in reached_nodes:
                continue
            nodes_in_cluster = node.get_reachable_nodes()
            reached_nodes = reached_nodes.union(nodes_in_cluster)

            edges_in_cluster = set()
            for nd in nodes_in_cluster:
                for edge in nd.edges:
                    edges_in_cluster.add(edge)

            self.clusters.append(Cluster(nodes_in_cluster, edges_in_cluster))

    def mean_cluster_dispersion(self):
        dx = []
        dy = []

        for cluster in self.clusters:
            dx.append(cluster.get_cluster_dispersion()[0])
            dy.append(cluster.get_cluster_dispersion()[1])

        dx = st.mean(dx)
        dy = st.mean(dy)

        return dx, dy

    def get_number_of_clusters(self):
        return len(self.clusters)

    def get_number_of_saccades(self):
        return len(self.saccades)


if __name__ == '__main__':
    keys, vals = db.breakup_stimuli("11.csv")

    fignum = 0


    for name in keys:
        g = gh.Graph()
        lista = pt.generate_points(vals[name])
        saccades = imst.imst(lista, 30, 5, 3, 1, 5)
        g.primm(lista)

        cl = Clusters(g, saccades)

        print(name)
        print("No of nodes:" + str(len(cl.g.nodes)))

        fig = plt.figure(fignum)
        ax = fig.add_subplot(111)
        path = name.translate({ord(t): None for t in '1234567890() '})
        img = plt.imread("pairs of animals/" + path + ".jpg")
        ax.imshow(img, extent=[0 + 448, 1024 + 448, 0 + 156, 768 + 156])
        for point in lista:
            if point.index in saccades:
                ax.plot(point.x, point.y, 'ro', markersize=5)
        for cluster in cl.clusters:
            print("CL: " + str(len(cluster.nodes)))
            for ed in cluster.edges:
                xs = []
                ys = []
                for nod in ed.connections:
                    xs.append(nod.point.x)
                    ys.append(nod.point.y)
                ax.plot(xs, ys, color='gray')
            for nd in cluster.nodes:
                ax.plot(nd.point.x, nd.point.y, 'bo', markersize=2)
        fig.canvas.draw()

        fignum += 1

plt.show()
