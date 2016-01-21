import random

from math import sqrt

from boids.boid import Boid


class BoidWorld:
    def __init__(self, size):
        self.x_size, self.y_size = size
        self.size = size
        self.boids = []
        self.radius = 50

    def add_boid(self):
        x, y = random.randrange(0, self.x_size), random.randrange(0, self.y_size)
        b = Boid((x, y), 10, self)
        self.boids.append(b)

    def remove_boid(self):
        if self.boids:
            self.boids.pop(0)

    def update(self):
        for boid in self.boids:
            boid.update()
            x, y = boid.position
            boid.position = x%self.x_size, y%self.y_size

    def get_neighbours(self, boid):
        # Must return only within a certain radius
        bs = []

        for b in self.boids:
            if b == boid:
                continue
            if self.within_radius(boid.position, b.position, self.radius):
                bs.append(b)

        return bs

    @staticmethod
    def within_radius(a, b, r):
        ax, ay = a
        bx, by = b

        if sqrt((bx-ax)**2+(by-ay)**2) < r:
            return True

        return False
