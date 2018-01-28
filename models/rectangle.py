from models.element import Element
from geometry.move import Move
from geometry.rotate import Rotate
from math import cos, sin, radians

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
		
    def rotate_point(self, point, angle, center_point=(0, 0)):
        angle_rad = radians(angle % 360)
        # Shift the point so that center_point becomes the origin
        new_point = (point[0] - center_point[0], point[1] - center_point[1])
        new_point = (new_point[0] * cos(angle_rad) - new_point[1] * sin(angle_rad),
        new_point[0] * sin(angle_rad) + new_point[1] * cos(angle_rad))
        # Reverse the shifting we have done
        new_point = (new_point[0] + center_point[0], new_point[1] + center_point[1])
        return new_point
	
    def rotate(self, alpha):
        centerX = self.posX + (self.width / 2)
        centerY = self.posY + (self.height / 2)
        new_coord = self.rotate_point((self.posX, self.posY), alpha, (centerX, centerY))
        self.posX = new_coord[0]
        self.posY = new_coord[1]
		
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