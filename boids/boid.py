import random
from math import sin, cos, radians


class Boid:
    id_counter = 0  # Used to give each boid a unique

    def __init__(self, pos, vel, world):
        self.position = pos
        self.velocity = vel
        self.angle = radians(random.randrange(0, 360))
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
        # Still needs some "latency"

        if not neighbours:
            return

        s = 0
        for n in neighbours:
            s += n.angle

        avg = s/len(neighbours)

        self.angle = avg
