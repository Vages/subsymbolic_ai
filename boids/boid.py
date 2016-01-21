import random
from math import sin, cos


class Boid:
    def __init__(self, pos, vel):
        self.position = pos
        self.velocity = vel
        self.angle = random.randrange(0, 360)

    def move(self):
        dx, dy = self.velocity*cos(self.angle), self.velocity*sin(self.angle)
        x, y = self.position
        self.position = x+dx, y+dy

    def update(self):
        self.move()