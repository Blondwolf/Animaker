import pygame
from pygame.locals import *
from pygame.locals import QUIT, MOUSEBUTTONDOWN, KEYDOWN, K_RETURN
if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.draw.circle(screen, [155, 0, 142], (50, 50), 20)
    pygame.draw.rect(screen, [124, 124, 142], (150, 200, 100, 40))
    pygame.draw.polygon(screen, [0, 255, 0], [(120, 120), (80, 80), (160, 80)])
    pygame.draw.circle(screen, [155, 0, 142], (100, 100), 20)
    pygame.draw.rect(screen, [124, 124, 142], (200, 250, 100, 40))
    pygame.draw.polygon(screen, [0, 255, 0], [(170, 170), (130, 130), (210, 130)])
    pygame.display.flip()
    running = 1
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = 0
