import pygame
from pygame.locals import *
from pygame.locals import QUIT, MOUSEBUTTONDOWN, KEYDOWN, K_RETURN
if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.draw.circle(screen, [0, 0, 255], (50, 50), 20)
    pygame.draw.rect(screen, [0, 0, 255], (150, 200, 100, 40))
    pygame.draw.polygon(screen, [0, 0, 255], [(120, 120), (80, 80), (160, 80)])
    pygame.draw.circle(screen, [0, 0, 255], (100, 100), 20)
    pygame.draw.rect(screen, [0, 0, 255], (200, 250, 100, 40))
    pygame.draw.polygon(screen, [0, 0, 255], [(170, 170), (130, 130), (210, 130)])
    pygame.display.flip()
    running = 1
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = 0
