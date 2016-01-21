import random

from boids.boid import Boid


class BoidWorld:
    def __init__(self, size):
        self.x_size, self.y_size = size
        self.size = size
        self.boids = []

    def add_boid(self):
        x, y = random.randrange(0, self.x_size), random.randrange(0, self.y_size)
        b = Boid((x, y), 0)
        self.boids.append(b)

    def remove_boid(self):
        self.boids.pop(0)