import pygame
from pygame.locals import *
from pygame.locals import QUIT, MOUSEBUTTONDOWN, KEYDOWN, K_RETURN


# http://www.pygame.org/docs/ref/draw.html#pygame.draw.polygon
if __name__ == '__main__':
	pygame.init()

	# open windows with size
	screen = pygame.display.set_mode((640, 480))
	
	# Draw circle (screen, color, posX, posY, radius)
	pygame.draw.circle(screen, [0, 0, 255], (50, 50), 20)
	
	# Draw rectangle (screen, color, Rect(posx, posy, width, height), width=0)
	pygame.draw.rect(screen, [255, 255, 255], (150, 200, 100, 40))
	
	# Draw triangle (screen, color, ((x, y), (x2, y2), (x3, y3), width=0)
	pygame.draw.polygon(screen, [255, 0, 0], [(120, 120), (80, 80), (160, 80)])
	
	# refresh screen
	pygame.display.flip()

	# Infinite loop
	running = 1
	while running:
		for event in pygame.event.get():
			if event.type == QUIT:
				running = 0