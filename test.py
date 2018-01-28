import pygame, time, sys
from pygame.locals import *
from pygame.locals import QUIT, MOUSEBUTTONDOWN, KEYDOWN, K_RETURN
from models.ball import Ball
from models.triangle import Triangle
from models.rectangle import Rectangle

def refresh_screen(objects, pygame, screen):
    for obj in objects:
        obj.draw(pygame, screen)

if __name__ == '__main__':
    pygame.init()
    objects=[]
    screen = pygame.display.set_mode((800, 600))
    tick=80
    ball0 = Ball(750, 550, 20, [0, 255, 255])
    objects.append(ball0)
    rect0 = Rectangle(10, 400, 100, 25, [255, 255, 255])
    objects.append(rect0)
    t = 10
    while(t):
        screen.fill(0)
        print(t)
        p = 10
        ball0.translate(-50, -50)
        ball0.draw(pygame, screen)
        rect0.rotate(1.5707)
        rect0.draw(pygame, screen)
        while(p):
            screen.fill(0)
            ball0.translate(5, 5)
            ball0.draw(pygame, screen)
            p = p - 2
            c = 2
            while(c):
                screen.fill(0)
                c = c - 1
                refresh_screen(objects, pygame, screen)
                pygame.display.update()
                time.sleep(tick/1000)
                for event in pygame.event.get():
                    if event.type == QUIT:
                        sys.exit(0)
            refresh_screen(objects, pygame, screen)
            pygame.display.update()
            time.sleep(tick/1000)
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit(0)
        t = t - 1
        refresh_screen(objects, pygame, screen)
        pygame.display.update()
        time.sleep(tick/1000)
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
    screen = pygame.display.set_mode((800, 600))
    pygame.display.flip()
    running = 1
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = 0
        for obj in objects:
            obj.move()
            obj.draw(pygame, screen)
            refresh_screen(objects, pygame, screen)
            pygame.display.update()
            time.sleep(tick/1000)
