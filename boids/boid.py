import random
from math import sin, cos, pi, atan2, hypot
from random import random


class Boid:
    id_counter = 0  # Used to give each boid a unique

    def __init__(self, pos, vel, world):
        self.position = pos
        self.angle = random()*2*pi
        self.velocity = (vel*cos(self.angle), vel*sin(self.angle))
        self.world = world
        self.id = Boid.id_counter
        Boid.id_counter += 1

    def __eq__(self, other):
        if self.id == other.id:
            return True
        return False

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return "boid " + str(self.id) + " @ " + str(self.position)

    def get_x(self):
        return self.position[0]

    def get_y(self):
        return self.position[1]

    def update(self):
        neighbours = self.world.get_neighbours(self)

        align = self.calculate_alignment_force(neighbours)

        self.velocity = [sum(x) for x in zip(self.velocity, align)]
        self.angle = atan2(self.velocity[1], self.velocity[0]) # adjust angle

        self.move()

    def calculate_alignment_force(self, neighbours):
        if not neighbours:
            return 0, 0

        sin_sum = 0
        cos_sum = 0

        for n in neighbours:
            sin_sum += sin(n.angle)
            cos_sum += cos(n.angle)

        h = hypot(sin_sum, cos_sum)
        cur_cos, cur_sin = cos(self.angle), sin(self.angle)

        diff_x, diff_y = cos_sum/h-cur_cos, sin_sum/h-cur_sin

        return self.world.alignment_weight*diff_x, self.world.alignment_weight*diff_y

    def move(self):
        self.position = [sum(x) for x in zip(self.position, self.velocity)]

