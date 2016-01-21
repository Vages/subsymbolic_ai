import random
from math import sin, cos, pi, atan2
from random import random


class Boid:
    id_counter = 0  # Used to give each boid a unique

    def __init__(self, pos, vel, world):
        self.position = pos
        self.velocity = vel
        self.angle = random()*2*pi
        self.world = world
        self.id = Boid.id_counter
        Boid.id_counter += 1

    def __eq__(self, other):
        if self.id == other.id:
            return True
        return False

    def __hash__(self):
        return hash(self.id)

    def move(self):
        dx, dy = self.velocity*cos(self.angle), self.velocity*sin(self.angle)
        x, y = self.position
        self.position = x+dx, y+dy

    def update(self):
        neighbours = self.world.get_neighbours(self)
        self.align(neighbours)
        self.move()

    def align(self, neighbours):
        if not neighbours:
            return

        sin_sum = 0
        cos_sum = 0

        for n in neighbours:
            sin_sum += sin(n.angle)
            cos_sum += cos(n.angle)

        avg_angle = atan2(sin_sum, cos_sum) % pi  # Average of neighbours

        diff = avg_angle-self.angle

        if 0 < abs(diff) <= pi:
            self.angle += diff*self.world.alignment_weight
            self.angle %= 2*pi

        elif diff < 0:
            diff += 2*pi
            self.angle += diff*self.world.alignment_weight
            self.angle %= 2*pi

        else:
            diff -= 2*pi
            self.angle += diff*self.world.alignment_weight
            self.angle %= 2*pi

