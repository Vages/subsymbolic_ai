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

        for boid in self.world.boids:
            self.draw_boid(boid)

        pygame.display.flip()

    def draw_boid(self, boid):
        pygame.draw.circle(self.screen, (255, 255, 255), boid.position, 10)

if __name__ == "__main__":
    pygame.init()
    bw = BoidWorld((300, 300))
    bg = BoidGraphics(bw, 30)
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
