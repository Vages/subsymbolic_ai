from math import sin, cos, pi, hypot
from random import random
import numpy as np

class Boid:
    id_counter = 0  # Used to give each boid a unique
    max_speed = 20
    max_acceleration = 10

    def __init__(self, pos, vel, world):
        self.position = np.array(pos)
        angle = random()*2*pi
        self.velocity = np.array((vel*cos(angle), vel*sin(angle)))
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

        self.velocity = self.velocity + align

        self.position = self.position + self.velocity

    def calculate_alignment_force(self, neighbours):
        if not neighbours:
            return 0, 0

        s = np.array((.0,.0))

        for n in neighbours:
            s += n.velocity

        s = Boid.normalize(s, magnitude=Boid.max_speed)
        steer = s-self.velocity
        steer = Boid.limit_vector(steer, limit=Boid.max_acceleration)
        return steer


    @staticmethod
    def normalize(v, magnitude=1):
        norm = np.linalg.norm(v)
        if norm == 0:
            return v

        return v*magnitude/norm

    @staticmethod
    def subtract_vector(a, b):
        a_x, a_y = a
        b_x, b_y = b
        return a_x-b_x, a_y-b_y

    @staticmethod
    def limit_vector(v, limit):
        norm = np.linalg.norm(v)
        if norm > limit:
            return Boid.normalize(v, limit)

        return v
