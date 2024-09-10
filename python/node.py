import math


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.parent = None
        self.H = 0
        self.G = 10000000000
        self.children = []
        self.is_obstacle = False
        self.is_start = False
        self.is_goal = False

    def cost(self):
        if self.parent:
            return math.sqrt(((self.x - self.parent.x) ** 2) + ((self.y - self.parent.y) ** 2))
        else:
            return 0

    def isObstacle(self):
        return self.is_obstacle

    def setObstacle(self):
        self.is_obstacle = True

    def isStart(self):
        return self.is_start

    def setStart(self):
        self.is_start = True

    def isGoal(self):
        return self.is_goal

    def setGoal(self):
        self.is_goal = True
