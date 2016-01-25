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
        x, y = boid.position
        x, y = round(x), round(y)
        pygame.draw.circle(self.screen, (255, 255, 255), (x, y), self.BOID_RADIUS)
        ang = boid.angle
        ang_cos = cos(ang)
        ang_sin = sin(ang)
        pygame.draw.line(self.screen, (0, 0, 0), (x, y), (x+ang_cos*self.BOID_RADIUS, y + ang_sin*self.BOID_RADIUS), 3)


if __name__ == "__main__":
    pygame.init()
    bw = BoidWorld((1280, 720))
    bg = BoidGraphics(bw, 30)
    for i in range(20):
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
