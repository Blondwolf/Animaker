from models.element import Element
from geometry.move import Move
from geometry.rotate import Rotate

class Ball(Element):
    def __init__(self, posX, posY, radius, color=[255,255,255]):
        self.posX = posX
        self.posY = posY
        self.radius = radius
        self.color = color
        self.moves = []
        self.rotates = []

    def center(self):
        return self.posX, self.posY
		
    def draw(self, pygame, screen):
        pygame.draw.circle(screen, self.color, (self.posX, self.posY), self.radius)

    def add_move(self, x, y):
        self.moves.append(Move(x, y))
	
    def translate(self, x, y):
        self.posX += x
        self.posY += y
		
    # useless rotate a circle 
    def rotate(self, alpha):
        pass
		
    def move(self):
        if len(self.moves) > 0:
            move = self.moves[0]
            translate = move.move()
            self.posX += translate[0]
            self.posY += translate[1]
            if move.finish:
                self.moves.pop(0)
		
    def __str__(self):
         return "Ball({}, {}, {}, {})".format(self.posX, self.posY, self.radius, self.color)