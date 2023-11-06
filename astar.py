import random
import math
import time
from tkinter import *


class Node():

    h = 0
    g = 10000
    f = 0
    parent = 0
    verified = False

    def __init__(self, point) -> None:
        self.point = point

class Astar:
    
    def __init__(self, start, goal, board) -> None:
        self.start = start
        self.goal = goal
        self.board = board
        self.createNodeMap()

    def createNodeMap(self):
        self.nodes = list()
        for i in enumerate(self.board):
            self.nodes.append(list())
            for j in enumerate(self.board[0]):
                self.nodes[-1].append(None)
        
    def getpath(self, node):
        coords = list()
        while True:
            if node.parent == 0:
                break
            coords.append(node.point)
            node = node.parent
        return coords
    
    def astar(self):
        openSet = [Node(self.start)]
        openSet[0].g = 0
        cameFrom = list()
        
        while len(openSet) > 0:
            current = openSet[0]
            if current.point == self.goal:
                return self.getpath(current)
            
            openSet.pop(0)
            neighbor = self.getNeighbor(current.point)
            for i, n in enumerate(neighbor):
                tg = current.g + self.dist(current.point, n.point)
                if tg < n.g:
                    n.parent = current
                    n.g = tg
                    n.f = tg + self.dist(n.point, self.goal)
                    if openSet.count(n) == 0:
                        openSet.append(n)
        return False
        
    
    def getNeighbor(self, point):
        nodes = list()
        x, y = point
        for i in range(y-1, y+2):
            for j in range(x-1, x+2):
                if i == y and j == x:
                    continue
                if i < 0 or i >= len(self.board):
                    continue
                if j < 0 or j >= len(self.board[0]):
                    continue
                if self.board[i][j] == "x":
                    continue

                if self.nodes[i][j] == None:
                    self.nodes[i][j] = Node([j, i])
                    
                if type(self.nodes[i][j]) == Node:
                    nodes.append(self.nodes[i][j])
        return nodes

    def dist(self, start, end):
        x1, y1 = start
        x2, y2 = end
        return int(math.sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2)) * 10)
        

class Board:
    start = None
    goal = None
    fields = list()
    
    def __init__(self, x, y) -> None:
        self.size_x = x
        self.size_y = y
        self.gen_board(x, y)
        pass
    
    def gen_board(self, x, y):
        if x < 1 or x > 100:
            return False
        if y < 1 or y > 100:
            return False
        
        for i in range(y):
            self.fields.append(list())
            for j in range(x):
                if random.random() > 0.7:
                    self.fields[i].append("x")
                else:
                    self.fields[i].append("o")
        self.start = [0,0]
        self.fields[0][0] = "s"
        self.goal = [x-1 , y-1]
        self.fields[y-1][x-1] = "e"

    def setStart(self, new_start):
        x, y = new_start
        if x < 0 or x > self.size_x:
            return False
        if y < 0 or y > self.size_y:
            return False
        
        ox, oy = self.start
        self.fields[oy][ox] = "o"
        self.start = new_start
        self.fields[y][x] = "s"
        return True
    
    def setGoal(self, new_goal):
        x, y = new_goal
        if x < 0 or x > self.size_x:
            return False
        if y < 0 or y > self.size_y:
            return False
        
        ox, oy = self.goal
        self.fields[oy][ox] = "o"
        self.goal = new_goal
        self.fields[y][x] = "e"
        return True
    
    def changeObsticle(self, coords):
        x, y = coords
        if x < 0 or x > self.size_x:
            return False
        if y < 0 or y > self.size_y:
            return False
        
        if self.fields[y][x] == "o":
            self.fields[y][x] = "x"
            return True
        if self.fields[y][x] == "x":
            self.fields[y][x] = "o"
            return True
        
        
class Window():
    
    def __init__(self) -> None:
        self.rootWindow = Tk()
        self.rootWindow.geometry("1000x800")
        self.rootWindow.resizable(0, 0)
        self.rootWindow.title("A-Star algoritm")

        self.board = Board(50, 40)
        self.drawBoard()
        self.rootWindow.bind("<Button>", self.mouse)


        self.rootWindow.mainloop()
        
    def drawBoard(self):
        self.windowBoard = Canvas(self.rootWindow, width=1000, height=800)
        self.windowBoard.configure(bg="#fff")
        self.windowBoard.pack()
        self.refreshBoard()

    def drawPath(self):
        board = self.board.fields.copy()
        path = Astar(self.board.start, self.board.goal, board).astar()
        if not path:
            return
        
        for i, p in enumerate(path):
            x, y = p
            if p != self.board.goal:
                tag = (str("{}x{}").format(x+1, y+1))
                item = self.windowBoard.find_withtag(tag)
                self.windowBoard.itemconfigure(tag, fill="yellow")
        
        
    
    def refreshBoard(self):
        a = 0
        b = 0
        for i, y in enumerate(self.board.fields):
            for j, x in enumerate(y):
                if x == "o": fill = "white"
                if x == "x": fill = "black"
                if x == "s": fill = "green"
                if x == "e": fill = "red"
                
                tag = (str("{}x{}").format(j+1, i+1))
                item = self.windowBoard.find_withtag(tag)
                if item:
                    a += 1
                    self.windowBoard.itemconfigure(tag, fill=fill)
                else:
                    b += 1
                    self.windowBoard.create_rectangle(j * 20, i * 20, (j + 1) * 20, (i + 1) * 20, fill=fill, tags=tag)
        self.drawPath()

    def mouse(self, event):
        num = event.num
        x = int(event.x / 20)
        y = int(event.y / 20)
        if num == 1:
            self.board.setStart([x, y])
        if num == 2:
            self.board.changeObsticle([x, y])
        if num == 3:
            self.board.setGoal([x, y])
        self.refreshBoard()

w = Window()
