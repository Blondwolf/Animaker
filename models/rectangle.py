from models.element import Element
from geometry.move import Move
from geometry.rotate import Rotate
from math import cos, sin, radians

class Rectangle(Element):
    def __init__(self, posX, posY, width, height, color=[255, 255, 255]):
        self.posX = posX
        self.posY = posY
        self.posX2 = posX
        self.posY2 = posY + height
        self.posX3 = posX + width
        self.posY3 = posY + height
        self.posX4 = posX + width
        self.posY4 = posY
        self.width = width
        self.height = height
        self.color = color
        self.moves = []
        self.rotates = []

    def center(self):
        return (self.posX+self.width)/2, (self.posY+self.height)/2
		
    def draw(self, pygame, screen):
        pygame.draw.polygon(screen, self.color, [(self.posX, self.posY), (self.posX2, self.posY2), (self.posX3, self.posY3), (self.posX4, self.posY4)])
		
    def add_move(self, x, y):
        self.moves.append(Move(x, y))
	
    def rotate_point(self, x, y, centerX, centerY, alpha):	
        s = sin(alpha)
        c = cos(alpha)
        x -= centerX
        y -= centerY
        new_x = x * c - y * s
        new_y = x * s + y * c
        x = new_x + centerX
        y = new_y + centerY
        return x, y
		
    def rotate(self, alpha):
        centerX = self.posX + (self.width / 2)
        centerY = self.posY + (self.height / 2)
        self.posX, self.posY = self.rotate_point(self.posX, self.posY, centerX, centerY, alpha)
        self.posX2, self.posY2 = self.rotate_point(self.posX2, self.posY2, centerX, centerY, alpha)
        self.posX3, self.posY3 = self.rotate_point(self.posX3, self.posY3, centerX, centerY, alpha)
        self.posX4, self.posY4 = self.rotate_point(self.posX4, self.posY4, centerX, centerY, alpha)
		
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