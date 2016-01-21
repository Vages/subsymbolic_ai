import pygame
import sys

from boids.boid_world import BoidWorld


class BoidGraphics:

    def __init__(self, world, fps):
        self.world = world
        self.screen = pygame.display.set_mode(self.world.size)
        self.clock = pygame.time.Clock()
        self.fps = fps

    def draw(self):
        self.clock.tick(self.fps)

        self.screen.fill((0, 0, 0))

        pygame.display.flip()

if __name__ == "__main__":
    pygame.init()
    bw = BoidWorld((300, 300))
    bg = BoidGraphics(bw, 30)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        bg.draw()

