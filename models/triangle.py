from models.element import Element
from geometry.move import Move
from geometry.rotate import Rotate

class Triangle(Element):
    def __init__(self, posX1, posY1, posX2, posY2, posX3, posY3, color=[255,255,255]):
        self.posX = posX1
        self.posY = posY1
        self.posX2 = posX2
        self.posY2 = posY2
        self.posX3 = posX3
        self.posY3 = posY3
        self.color = color
        self.moves = []
        self.rotates = []

    def center(self):
        return (self.posX+self.posX2+self.posX3)/3, (self.posY+self.posY2+self.posY3)/3
		
    def draw(self, pygame, screen):
        pygame.draw.polygon(screen, self.color, [(self.posX, self.posY), (self.posX2, self.posY2), (self.posX3, self.posY3)])
		
    def add_move(self, x, y):
        self.moves.append(Move(x, y))
		
    def add_rotate(self, alpha):
        pass
	
    def translate(self, x, y):
        self.posX += x
        self.posY += y
        self.posX2 += x
        self.posY2 += y
        self.posX3 += x
        self.posY3 += y
		
    def move(self):
        if len(self.moves) > 0:
            move = self.moves[0]
            translate = move.move()
            self.posX += translate[0]
            self.posY += translate[1]
            self.posX2 += translate[0]
            self.posY2 += translate[1]
            self.posX3 += translate[0]
            self.posY3 += translate[1]
            if move.finish:
                self.moves.pop(0)
		
    def __str__(self):
         return "Triangle({}, {}, {}, {}, {}, {}, {})".format(self.posX, self.posY, self.posX2, self.posY2, self.posX3, self.posY3, self.color)