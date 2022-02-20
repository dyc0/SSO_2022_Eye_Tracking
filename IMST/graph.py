# -*- coding: utf-8 -*-
"""
Created on Sun Feb 13 15:06:05 2022

@author: Duca
"""

import copy
import math
from queue import Queue
import database_obrada as db
import points as pt
from matplotlib import pyplot as plt

class Node:
    
    def __init__(self, point):
        self.point = point
        self.edges = []
        
    def add_edge(self, edge):
        self.edges.append(edge)
        
    def check_branching_depth(self, start_edge, depth):        
        current_depth = 0
        is_deeper = False
        
        for edge in self.edges:
            if edge == start_edge:
                continue
            
            current_depth += 1
            if current_depth >= depth:
                return True
            
            curnode = [nd for nd in edge.connections if nd is not self]
            curnode = curnode[0]
            
            is_deeper = curnode.check_branching_depth(edge, depth-1)
            
        return is_deeper

    """
    def get_reachable_nodes(self, reached_nodes=set()):
        if not reached_nodes:
            reached_nodes.add(self)
            
        for edge in self.edges:
            for node in edge.connections:
                if node not in reached_nodes:
                    reached_nodes.add(node)
                    reached_nodes = \
                        reached_nodes.union(node.get_reachable_nodes(reached_nodes))
                    
        return reached_nodes
    """

    def get_reachable_nodes(self):
        nodes_to_check = Queue()
        reached_nodes = set()
        nodes_to_check.put(self)

        while not nodes_to_check.empty():
            current_node = nodes_to_check.get()
            reached_nodes.add(current_node)

            for edge in current_node.edges:
                for node in edge.connections:
                    if node in reached_nodes:
                        continue
                    else:
                        nodes_to_check.put(node)

        return reached_nodes
        
    def __str__(self):
        node_print = "( " + str(self.point.index) + "|" + str(self.point) + ",\n Edges: "
        for edge in self.edges:
            node_print += str(edge) + ",\n"
        node_print += ")"
        return node_print
        
        
class Edge:
    
    def __init__(self, node1, node2, length = -1):
        self.connections = {node1, node2}
        self.length = length
        if self.length == -1:
            self.length = node1.point - node2.point
        
            
    def get_neighbour_edges(self, depth, neighbours = set(), visited_nodes = set()):
        if depth == 0:
            return neighbours
        
        if not neighbours:
            neighbours.add(self)
        
        for node in self.connections:
            if node in visited_nodes:
                continue
            visited_nodes.add(node)
            
            for edge in node.edges:
                if edge in neighbours:
                    continue
                neighbours.add(edge)
                neighbours = neighbours.union(\
                        edge.get_neighbour_edges(depth-1, neighbours, visited_nodes))        
        
        return neighbours
            
    def __str__(self):
        edge_print = "["
        first = True
        for e in self.connections:
            edge_print += str(e.point.index)
            if first:
                edge_print += " <--> "
                first = False
        edge_print += "]"
        return edge_print
        


class Graph:

    def __init__(self):
        self.nodes = []
        self.edges = []
        self.node_indexes = []
        
    def add_node(self, node):
        self.nodes.append(node)
        self.node_indexes.append(node.point.index)
        self.node_indexes.sort()        

    def add_edge(self, node1, node2, length = -1):
        new_edge = Edge(node1, node2, length)
        self.edges.append(new_edge)
        node1.add_edge(new_edge)
        node2.add_edge(new_edge)

    def primm(self, input_points):
        points = copy.deepcopy(input_points)
        root = points[0]
        points.remove(root)
        self.add_node(Node(root))
        
        while points:
            min_distance = math.inf
            
            for node in self.nodes:
                for point in points:
                    distance = node.point - point
                    if distance < min_distance:
                        min_distance = distance
                        min_node = node
                        min_point = point
            
            new_node = Node(min_point)
            self.add_node(new_node)
            self.add_edge(min_node,new_node, min_distance)
            
            points.remove(min_point)
            
    @staticmethod
    def order_nodes(node):
        return node.point.index
    
    def get_nodes_ordered(self):
        self.nodes.sort(key=Graph.order_nodes)

    def remove_node(self, node_to_remove):
        edges_to_remove = [edge for edge in self.edges\
                           if node_to_remove in edge.connections]
        
        for edge in edges_to_remove:
            self.remove_edge(edge)

        self.node_indexes.remove(node_to_remove.point.index)
        self.nodes.remove(node_to_remove)
            
        
    def remove_edge(self, edge):
        for node in edge.connections:
            node.edges.remove(edge)
        self.edges.remove(edge)
    
            
    def __str__(self):
        printed_graph = "Nodes: \n"
        for node in self.nodes:
            printed_graph += str(node) + "\n\n"
        return printed_graph
            

if __name__ == '__main__':
    keys, vals = db.breakup_stimuli("31.csv")
    
    for name in keys:
        break
        g = Graph()
        lista = pt.generate_points(vals[name])
        g.primm(lista)
        print(g)
        
        fignum = 0
        fig = plt.figure(fignum)
        ax = fig.add_subplot(111)
        path = name.translate({ord(t): None for t in '1234567890() '})
        img = plt.imread("pairs of animals/" + path + ".jpg")
        ax.imshow(img, extent=[0+448, 1024+448, 0+156, 768+156])
        for node in g.nodes:
            ax.plot(node.point.x, node.point.y, 'ro')
        for edge in g.edges:
            coordinates_x = [node.point.x for node in edge.connections]
            coordinates_y = [node.point.y for node in edge.connections]
            ax.plot(coordinates_x, coordinates_y)
        fig.canvas.draw()
        plt.show()
        
        fignum+=1
        
    ''' 
    g = Graph()
    lista = pt.generate_points(vals[name])
    g.primm(lista)
    for n in g.get_nodes_ordered():
        print(n)
        print("\n\n")'''
        
    g = Graph()
    lista = pt.generate_points(vals[name])
    g.primm(lista)
    for node in g.nodes:
        edge = node.edges[0]
        if node.check_branching_depth(edge, 3):
            print(edge.get_neighbour_edges(3))
            print(node)
    
    
    