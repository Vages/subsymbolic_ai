from math import sin, cos, pi, hypot
from random import random


class Boid:
    id_counter = 0  # Used to give each boid a unique
    MAX_SPEED = 20
    MAX_ACCELERATION = 10

    def __init__(self, pos, vel, world):
        self.position = pos
        angle = random()*2*pi
        self.velocity = (vel*cos(angle), vel*sin(angle))
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

        self.move()

    def calculate_alignment_force(self, neighbours):
        if not neighbours:
            return 0, 0

        x_sum, y_sum = 0, 0

        for n in neighbours:
            v_x, v_y = n.velocity
            x_sum += v_x
            y_sum += v_y

        x_sum, y_sum = Boid.normalize(x_sum, y_sum, magnitude=Boid.MAX_SPEED)
        steer = Boid.subtract_vector((x_sum, y_sum), self.velocity)
        steer = Boid.limit_vector(steer, limit=Boid.MAX_ACCELERATION)
        return steer

    def move(self):
        self.position = [sum(x) for x in zip(self.position, self.velocity)]



    @staticmethod
    def normalize(a, b, magnitude=1):
        h = hypot(a, b)
        return a*magnitude/h, b*magnitude/h

    @staticmethod
    def subtract_vector(a, b):
        a_x, a_y = a
        b_x, b_y = b
        return a_x-b_x, a_y-b_y

    @staticmethod
    def limit_vector(vector, limit):
        a, b = vector
        h = hypot(a, b)
        if h > limit:
            return Boid.normalize(a, b, limit)

        return vector