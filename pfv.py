#This file contains the implementations of various path-finding algorithms to be used in the visualizer.

import heapq #priority queue
import math

#necessary objects:
class node_data:
    def __init__(self):
        self.d = math.inf #smallest dist to adjacent node
        self.p = {0,0} #parent node
        self.k = False #discovered bool

class visualizer:
    def __init__(self):
        self.rows = 50
        self.cols = 50
        self.nodes = [[0]*cols]*rows
        self.node_data = [[node_data()]*cols]*rows 

    def runDijkstra(self):

    def runDFS(self):

    def runBFS(self):

