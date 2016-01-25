import numpy
import pygame
import sys

from math import cos, sin

from boids.boid_world import BoidWorld


class BoidGraphics:
    BOID_RADIUS = 10

    def __init__(self, world, fps):
        self.world = world
        self.screen = pygame.display.set_mode(self.world.size)
        self.clock = pygame.time.Clock()
        self.fps = fps

    def draw(self):
        self.clock.tick(self.fps)

        self.screen.fill((0, 0, 0))

        self.world.update()

        for boid in self.world.boids:
            self.draw_boid(boid)

        pygame.display.flip()

    def draw_boid(self, boid):
        integer_position = numpy.around(boid.position, 0).astype(int)
        pygame.draw.circle(self.screen, (255, 255, 255), integer_position, self.BOID_RADIUS)
        integer_speed = boid.normalize(boid.velocity, self.BOID_RADIUS).astype(int)
        pygame.draw.line(self.screen, (0, 0, 0), integer_position, integer_position+integer_speed, 3)


if __name__ == "__main__":
    pygame.init()
    bw = BoidWorld((1280, 720))
    bg = BoidGraphics(bw, 30)
    for i in range(200):
        bw.add_boid()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PLUS:
                    bw.add_boid()
                if event.key == pygame.K_MINUS:
                    bw.remove_boid()

        bg.draw()
