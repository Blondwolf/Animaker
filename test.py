import pygame
from pygame.locals import *
from pygame.locals import QUIT, MOUSEBUTTONDOWN, KEYDOWN, K_RETURN
from models.ball import Ball
from models.triangle import Triangle
from models.rectangle import Rectangle

if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((640, 480))
    objects=[]
    ball0 = Ball(50, 50, 20, [155, 0, 142])
    ball0.add_move(50, 0)
    objects.append(ball0)
    rect0 = Rectangle(150, 200, 100, 40, [124, 124, 142])
    rect0.add_move(80, 50)
    objects.append(rect0)
    triangle0 = Triangle(120, 120, 80, 80, 160, 80, [0, 255, 0])
    triangle0.add_move(50, 5)
    objects.append(triangle0)
    pygame.display.flip()
    running = 1
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = 0
        screen.fill(0)
        for obj in objects:
            obj.move()
            obj.draw(pygame, screen)
        pygame.display.flip()
        clock.tick(200)
