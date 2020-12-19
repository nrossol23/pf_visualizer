#This file contains the implementations of various path-finding algorithms to be used in the visualizer.
import heapq #priority queue
import math

#necessary objects:
class node_data:
    def __init__(self):
        self.d = math.inf #smallest dist to adjacent node
        self.p = (0,0) #parent node
        self.k = False #discovered

class visualizer:
    def __init__(self):
        self.rows = 50
        self.cols = 50
        #self.nodes = [[0]*cols]*rows
        self.data = [[node_data()]*cols]*rows 

    #helpers:
    def getAdj(x, y):
        adj = []
        if x > 0 and self.data[x-1][y].k == False: adj.append((x-1,y))
        if y > 0 and self.data[x][y-1].k == False: adj.append((x,y-1))
        if x < self.cols - 1 and self.data[x+1][y].k == False: adj.append((x+1,y))
        if y < self.rows - 1 and self.data[x][y+1].k == False: adj.append((x, y+1))
        return adj

    #reset nodes and data to default values
    def resetVisualizer(self):
        self.data = [[node_data()]*cols]*rows

    #get euclidean distance between two nodes\
    def getDist(x1, y1, x2, y2):


    def runDijkstra(self, xi, yi, xf, yf):
        pq = []
        start = (xi,y1)
        heappush(pq, (0, start)) #d of start vertex is 0
        self.data[xi][yi].d = 0;
        while len(pq) != 0:
            v0 = heappop(pq)[1] #idk if this is going to work? new to python syntax
            if v0[0] == xf and v0[1] == yf:
                return
            if self.data[v0[0]][v0[1]].k == False:
                self.data[v0[0]][v0[1]].k = True
                adj = getAdj(v0[0], v0[1])
                for vi in adj:
                    dist = self.data[v0[0]][v0[1]].d + getDist(vo[0], v0[1], vi[0], vi[1])
                    if dist < self.data[v1[0]][v1[1]].d:
                        self.data[v1[0]][v1[1]].d = dist
                        self.data[v1[0]][v1[1]].p = (v0[0], v0[1])
                        toPush = (v1[0], v1[1])
                        heappush(pq, (dist, toPush))


    #depth first search
    def runDFS(self, xi, yi, xf, yf):
        stack = []
        start = (xi,yi)
        stack.append(start)
        while len(stack) != 0:
            temp = stack.pop()
            if temp[0] == xf and temp[1] == yf: return
            self.data[temp[0]][temp[1]].k = True
            adj = getAdj(temp[0], temp[1])
            for p in adj: stack.append(p)
        
    #run breadth first search
    def runBFS(self, xi, yi, xf, yf):
        queue = []
        start = (xi, yi)
        queue.append(start)
        while len(queue) != 0:
            temp = queue.pop(0)
            if temp[0] == xf and temp[1] == yf: return
            self.data[temp[0]][temp[1]].k = True
            adj = getAdj(temp[0], temp[1])
            for p in adj: stack.append(p)           