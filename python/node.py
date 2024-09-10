import math


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.parent = None
        self.H = 0
        self.G = 10000000000
        self.children = []
        self.isObstacle = False
        self.start = False
        self.goal = False

    def cost(self):
        if self.parent:
            return math.sqrt(((self.x - self.parent.x) ** 2) + ((self.y - self.parent.y) ** 2))
        else:
            return 0

    def isObstacle(self):
        return self.isObstacle

    def setObstacle(self):
        self.isObstacle = True

    def isStart(self):
        return self.start

    def setStart(self):
        self.start = True

    def isGoal(self):
        return self.goal

    def setGoal(self):
        self.goal = True
