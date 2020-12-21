#This file contains the implementations of various path-finding algorithms to be used in the visualizer.
import heapq #priority queue
import pygame
import math

class visualizer:
    #store data for each node 
    class node_data:
        def __init__(self):
            self.d = math.inf #smallest dist to adjacent node
            self.p = (-1,-1) #parent node
            self.k = False #discovered
            self.w = False #is wall?

    def __init__(self):
        #colors:
        self.BLACK = (0,0,0)
        self.WHITE = (255,255,255)
        self.BLUE = (0,0,255)
        self.RED = (255,0,0)
        self.GREEN = (0,255,0) 
        self.DARKGREEN = (127,0,255) 


        #initialize pygame
        pygame.init()
        pygame.display.init()
        pygame.display.set_caption("Path Finding Visualizer")

        #GUI variables
        self.screen_width = 1098
        self.screen_height = 1098
        self.num_boxes = 50
        self.menu_height = 100
        self.box_size = 20
        self.margin = 2
        self.font = pygame.font.SysFont("Arial", 28)    
        self.screen = pygame.display.set_mode([self.screen_width, self.screen_height + self.menu_height])
        self.clock = pygame.time.Clock()

        #main algorithm variables:
        self.rows = 50
        self.cols = 50
        self.data = [[self.node_data() for j in range(self.cols)] for i in range(self.rows)]

    #initialize the base GUI layout
    def initializeGUI(self):
        self.screen.fill(self.BLACK)
        for i in range(0, self.screen_width, self.box_size+self.margin):
            for j in range(0, self.screen_height, self.box_size+self.margin):
                pygame.draw.rect(self.screen, self.WHITE, (i, j, self.box_size, self.box_size), 0)
        pygame.draw.rect(self.screen, self.WHITE, (0, self.screen_height + self.margin, self.screen_width, self.menu_height), 0)

    def resetMenu(self):
        pygame.draw.rect(self.screen, self.WHITE, (0, self.screen_height + self.margin, self.screen_width, self.menu_height), 0)

    #allow user to choose start and end point by clicking
    def interactGUI(self):
        start_chosen = False
        end_chosen = False
        xi = None
        xf = None
        yi = None
        yf = None

        while True:
            #event detection:
            clicked = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONUP:
                    clicked = True
                    pos = pygame.mouse.get_pos()

            self.resetMenu()
            if not start_chosen:
                word_surface = self.font.render('Choose Start Point', False, self.BLUE)
                self.screen.blit(word_surface, (self.screen_width/2 - 110, self.screen_height + self.menu_height/2))
            elif not end_chosen:
                word_surface = self.font.render('Choose End Point', False, self.BLUE)
                self.screen.blit(word_surface, (self.screen_width/2 - 110, self.screen_height + self.menu_height/2))
            else:
                #set up the buttons for choosing algorithm:
                button1 = pygame.draw.rect(self.screen, self.BLUE, (0 + self.screen_width/5 - 20, self.screen_height + self.menu_height/2, 175, 40), 0)
                button2 = pygame.draw.rect(self.screen, self.BLUE, (0 + (self.screen_width/5) * 2 - 20, self.screen_height + self.menu_height/2, 175, 40), 0)
                button3 = pygame.draw.rect(self.screen, self.BLUE, (0 + (self.screen_width/5) * 3 - 20, self.screen_height + self.menu_height/2, 175, 40), 0)
                button4 = pygame.draw.rect(self.screen, self.BLUE, (0 + (self.screen_width/5) * 4 - 20, self.screen_height + self.menu_height/2, 175, 40), 0)

                word_surface = self.font.render('Run BFS', False, self.WHITE)
                self.screen.blit(word_surface, (0 + self.screen_width/5, self.screen_height + self.menu_height/2))
                word_surface = self.font.render('Run DFS', False, self.WHITE)
                self.screen.blit(word_surface, (0 + (self.screen_width/5) * 2, self.screen_height + self.menu_height/2))
                word_surface = self.font.render('Run Dijkstra', False, self.WHITE)
                self.screen.blit(word_surface, (0 + (self.screen_width/5) * 3, self.screen_height + self.menu_height/2))
                word_surface = self.font.render('Restart', False, self.WHITE)
                self.screen.blit(word_surface, (0 + (self.screen_width/5) * 4, self.screen_height + self.menu_height/2))

            pygame.display.update()
            self.clock.tick(60)

            if clicked:
                if pos[1] < self.screen_height:
                    x = int(pos[0]/(self.box_size+self.margin))
                    y = int(pos[1]/(self.box_size+self.margin))
                    if not start_chosen: 
                        xi = x
                        yi = y
                        pygame.draw.rect(self.screen, self.GREEN, (x*(self.box_size + self.margin), y*(self.box_size + self.margin), self.box_size, self.box_size), 0)
                        start_chosen = True
                    elif not end_chosen: 
                        xf = x
                        yf = y
                        end_chosen = True
                        pygame.draw.rect(self.screen, self.RED, (x*(self.box_size + self.margin), y*(self.box_size + self.margin), self.box_size, self.box_size), 0)
                    else: #draw walls:
                        pygame.draw.rect(self.screen, self.BLACK, (x*(self.box_size + self.margin), y*(self.box_size + self.margin), self.box_size, self.box_size), 0)
                        self.data[x][y].w = True
                        print(x)
                        print(y)

                elif start_chosen and end_chosen:
                    #run proper algorithm
                    if button1.collidepoint(pos):
                        self.runBFS(xi, yi, xf, yf)
                    elif button2.collidepoint(pos):
                        self.runDFS(xi, yi, xf, yf)
                    elif button3.collidepoint(pos):
                        self.runDijkstra(xi, yi, xf, yf)
                    elif button4.collidepoint(pos):
                        self.resetVisualizer()
                        start_chosen = False
                        end_chosen = False
                    
                # self.visualize(xi,yi,xf,yf)
    
    #Get all adjacent nodes to given node
    def getAdj(self, x, y):
        adj = []
        if x > 0 and self.data[x-1][y].k == False and self.data[x-1][y].w == False: 
            adj.append((x-1,y)) 
        if y > 0 and self.data[x][y-1].k == False and self.data[x][y-1].w == False: 
            adj.append((x,y-1))
        if x < self.cols - 1 and self.data[x+1][y].k == False and self.data[x+1][y].w == False: 
            adj.append((x+1,y))
        if y < self.rows - 1 and self.data[x][y+1].k == False and self.data[x][y+1].w == False: 
            adj.append((x, y+1))
        if x < self.cols - 1 and y < self.rows - 1 and self.data[x+1][y+1].k == False and self.data[x+1][y+1].w == False:
            if self.data[x+1][y].w == False and self.data[x][y+1].w == False:
                adj.append((x+1, y+1))
        if x < self.cols - 1 and y > 0 and self.data[x+1][y-1].k == False and self.data[x+1][y-1].w == False:
            if self.data[x+1][y].w == False and self.data[x][y-1].w == False:
                adj.append((x+1, y-1))
        if x > 0 and y > 0 and self.data[x-1][y-1].k == False and self.data[x-1][y-1].w == False:
            if self.data[x-1][y].w == False and self.data[x][y-1].w == False:
                adj.append((x-1, y-1))
        if x > 0 and y < self.rows - 1 and self.data[x-1][y+1].k == False and self.data[x-1][y+1].w == False:
            if self.data[x-1][y].w == False and self.data[x][y+1].w == False:
                adj.append((x-1, y+1))
        return adj

    #reset nodes and data to default values
    def resetVisualizer(self):
        self.data = [[self.node_data() for j in range(self.cols)] for i in range(self.rows)]
        self.resetMenu()
        self.initializeGUI()

    #get euclidean distance between two nodes\
    def getDist(self, x1, y1, x2, y2):
        return math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))

    #display the path found to final node:
    def displayPath(self, xi, yi, xf, yf):
        x = xf
        y = yf
        while True:
            tempx = x
            tempy = y
            x = self.data[tempx][tempy].p[0]
            y = self.data[tempx][tempy].p[1]
            if x == xi and y == yi: break
            pygame.draw.rect(self.screen, self.DARKGREEN, (x*(self.box_size + self.margin), y*(self.box_size + self.margin), self.box_size, self.box_size), 0)
            pygame.display.update()
            self.clock.tick(60)

    #dijkstra's algorithm
    def runDijkstra(self, xi, yi, xf, yf):
        pq = []
        start = (xi,yi)
        heapq.heappush(pq, (0, start)) #d of start vertex is 0
        self.data[xi][yi].d = 0
        while len(pq) != 0:
            v0 = heapq.heappop(pq)[1] #is this is going to work? new to python syntax
            if v0[0] == xf and v0[1] == yf:
                self.displayPath(xi, yi, xf, yf)
                return
            if self.data[v0[0]][v0[1]].k == False:

                if v0[0] != xi or v0[1] != yi:
                    pygame.draw.rect(self.screen, self.BLUE, (v0[0]*(self.box_size + self.margin), v0[1]*(self.box_size + self.margin), self.box_size, self.box_size), 0)
                    pygame.display.update()
                    self.clock.tick(60)

                self.data[v0[0]][v0[1]].k = True
                adj = self.getAdj(v0[0], v0[1])
                for v1 in adj:
                    dist = self.data[v0[0]][v0[1]].d + self.getDist(v0[0], v0[1], v1[0], v1[1])
                    if dist < self.data[v1[0]][v1[1]].d:
                        self.data[v1[0]][v1[1]].d = dist
                        self.data[v1[0]][v1[1]].p = (v0[0], v0[1])
                        toPush = (v1[0], v1[1])
                        heapq.heappush(pq, (dist, toPush))

    #depth first search
    def runDFS(self, xi, yi, xf, yf):
        stack = []
        start = (xi,yi)
        stack.append(start)
        while len(stack) != 0:
            temp = stack.pop()
            if self.data[temp[0]][temp[1]].k == True: continue

            self.data[temp[0]][temp[1]].k = True
            if temp[0] == xf and temp[1] == yf: return

            if temp[0] != xi or temp[1] != yi:
                rect = pygame.draw.rect(self.screen, self.BLUE, (temp[0]*(self.box_size + self.margin), temp[1]*(self.box_size + self.margin), self.box_size, self.box_size), 0)
                pygame.display.update(rect)
                self.clock.tick(60)

            adj = self.getAdj(temp[0], temp[1])

            for p in adj: stack.append(p)
        
    #run breadth first search
    def runBFS(self, xi, yi, xf, yf):
        queue = []
        start = (xi, yi)
        queue.append(start)
        while len(queue) != 0:
            temp = queue.pop(0)
            if self.data[temp[0]][temp[1]].k == True: continue

            self.data[temp[0]][temp[1]].k = True
            if temp[0] == xf and temp[1] == yf: return

            if temp[0] != xi or temp[1] != yi:
                rect = pygame.draw.rect(self.screen, self.BLUE, (temp[0]*(self.box_size + self.margin), temp[1]*(self.box_size + self.margin), self.box_size, self.box_size), 0)
                pygame.display.update(rect)
                self.clock.tick(60)

            adj = self.getAdj(temp[0], temp[1])

            for p in adj: queue.append(p)      


#Run program:
program = visualizer()
program.initializeGUI()
program.interactGUI()