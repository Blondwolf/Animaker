from models.element import Element
from geometry.move import Move
from geometry.rotate import Rotate
import math

class Rectangle(Element):
    def __init__(self, posX, posY, width, height, color=[255, 255, 255]):
        self.posX = posX
        self.posY = posY
        self.width = width
        self.height = height
        self.color = color
        self.moves = []
        self.rotates = []

    def center(self):
        return (self.posX+self.width)/2, (self.posY+self.height)/2
		
    def draw(self, pygame, screen):
        pygame.draw.polygon(screen, self.color, [(self.posX, self.posY), (self.posX, self.posY + self.height), (self.posX + self.width, self.posY + self.height), (self.posX + self.width, self.posY)])
		
    def add_move(self, x, y):
        self.moves.append(Move(x, y))
		
    def rotate(self, alpha):
        centerX = self.posX + (self.width / 2)
        centerY = self.posY + (self.height / 2)
        self.posX = math.cos(alpha) * self.posX - math.sin(alpha) * self.posY
        self.posY = math.sin(alpha) * self.posX + math.cos(alpha) *self.posY
		
    def translate(self, x, y):
        self.posX += x
        self.posY += y
		
    def add_rotate(self, alpha):
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
         return "Rectangle({}, {}, {}, {}, {})".format(self.posX, self.posY, self.width, self.height, self.color)