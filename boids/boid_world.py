import random

from math import sqrt, hypot

from boids.boid import Boid


class BoidWorld:
    CONSTANTS = ((0, 0),)
    """
                 (-1, 0), (1, 0),
                 (0, 1), (0, -1),
                 (-1, -1), (-1, 1), (1, 1), (1, -1))
    """

    def __init__(self, size):
        self.x_size, self.y_size = size
        self.size = size
        self.boids = []
        self.flock_radius = 50
        self.alignment_weight = 1

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
            boid.position = x % self.x_size, y % self.y_size

    def get_neighbours(self, boid):
        bs = []

        for b in self.boids:
            if b == boid:
                continue

            for wx, wy in self.CONSTANTS:
                bx, by = b.position
                dx, dy = wx*self.x_size, wy*self.y_size

                if self.within_radius(boid.position, (bx+dx, by+dy), self.flock_radius):
                    bs.append(b)
                    break

        return bs

    @staticmethod
    def within_radius(a, b, r):
        ax, ay = a
        bx, by = b

        if hypot((bx-ax), (by-ay)) < r:
            return True

        return False
