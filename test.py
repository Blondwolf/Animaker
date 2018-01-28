import pygame
from pygame.locals import *
from pygame.locals import QUIT, MOUSEBUTTONDOWN, KEYDOWN, K_RETURN
if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.draw.circle(screen, [255, 255, 255], (20, 20), 50)
    pygame.draw.rect(screen, [255, 255, 255], (0, 50, 100, 100))
    pygame.display.flip()
    running = 1
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = 0
    pygame.display.flip()
    running = 1
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = 0
