import AST
from AST import addToClass
from functools import reduce
from models.ball import Ball
from models.rectangle import Rectangle
from models.triangle import Triangle

import math

operations = {
    '+' : lambda x,y: x+y,
    '-' : lambda x,y: x-y,
    '*' : lambda x,y: x*y,
    '/' : lambda x,y: x/y,
}

tick=100 # default
vars={}
objects={}

def write_header():
    file.write("import pygame\n")
    file.write("from pygame.locals import *\n")
    file.write("from pygame.locals import QUIT, MOUSEBUTTONDOWN, KEYDOWN, K_RETURN\n")
    file.write("from models.ball import Ball\n")
    file.write("from models.triangle import Triangle\n")
    file.write("from models.rectangle import Rectangle\n\n")

    file.write("if __name__ == '__main__':\n")
    file.write("    pygame.init()\n")
    file.write("    clock = pygame.time.Clock()\n")
    file.write("    screen = pygame.display.set_mode((640, 480))\n")
    file.write("    objects=[]\n")
	
def write_footer():
    file.write("    pygame.display.flip()\n")
    file.write("    running = 1\n")
    file.write("    while running:\n")
    file.write("        for event in pygame.event.get():\n")
    file.write("            if event.type == QUIT:\n")
    file.write("                running = 0\n")
    file.write("        screen.fill(0)\n")
    file.write("        for obj in objects:\n")
    file.write("            obj.move()\n")


@addToClass(AST.ProgramNode)
def execute(self):
    global file
    global objects
    global tick
    file = open("test.py", 'w')
    write_header()
    for c in self.children:
        c.execute()
    for key, values in objects.items():
        file.write("    {} = {}\n".format(key, values))
        for move in values.moves:
            file.write("    {}.add_move({})\n".format(key, str(move)))
        file.write("    objects.append({})\n".format(key))
    write_footer()
    file.write("            obj.draw(pygame, screen)\n")
    file.write("        pygame.display.flip()\n")
    file.write("        clock.tick({})\n".format(tick))
    
@addToClass(AST.TokenNode)
def execute(self):
    if isinstance(self.tok, str):
        try:
            return vars[self.tok]
        except KeyError:
            print("*** Error: variable %s undefined!" % self.tok)
    return self.tok
	
@addToClass(AST.ElementNode)
def execute(self):
    if isinstance(self.tok, str):
        try:
            return objects[self.tok]
        except KeyError:
            print("*** Error: variable %s undefined!" % self.tok)
    object_type = self.tok[0].lower()
    color = [255, 255, 255]
    length = len(self.tok)
    element = None
    if object_type == "ball":
        if length == 5:
            color = self.tok[4]
        element = Ball(self.tok[1], self.tok[2], self.tok[3], color)
    elif object_type == "rectangle":
        if length == 6:
            color = self.tok[5]
        element = Rectangle(self.tok[1], self.tok[2], self.tok[3], self.tok[4], color)
    elif object_type == "triangle":
        if length == 8:
            color = self.tok[7]
        element = Triangle(self.tok[1], self.tok[2], self.tok[3], self.tok[4], self.tok[5], self.tok[6], color)
    return element

@addToClass(AST.OpNode)
def execute(self):
    args = [c.execute() for c in self.children]
    if len(args) == 1:
        args.insert(0,0)
    return reduce(operations[self.op], args)

@addToClass(AST.AssignNode)
def execute(self):
    if self.children[1].type == "token":
        vars[self.children[0].tok] = self.children[1].execute()
    elif self.children[1].type == "element":
        objects[self.children[0].tok] = self.children[1].execute()

@addToClass(AST.PrintNode)
def execute(self):
    print (self.children[0].execute())
    
@addToClass(AST.WhileNode)
def execute(self):
    while self.children[0].execute():
        self.children[1].execute()
		
@addToClass(AST.ShowNode)
def execute(self):
    object_geom = objects.get(self.children[0].tok)
    file.write(object_geom.draw())
	
@addToClass(AST.IntNode)
def execute(self):
    return self.value
	
@addToClass(AST.FloatNode)
def execute(self):
    return self.value
		
@addToClass(AST.RotateNode)
def execute(self):
    object_geom = objects.get(self.children[0].tok)
    type = object_geom[0].lower()
    angle = self.children[1].execute()

    if type == "ball":
        pass
    if type == "rectangle":
        centerX = (object_geom[1]+object_geom[3])/2
        centerY = (object_geom[2]+object_geom[4])/2
        deltaX, deltaY = rotate_point(centerX, centerY, angle, object_geom[1], object_geom[2])
        deltaX2, deltaY2 = rotate_point(centerX, centerY, angle, object_geom[3], object_geom[4])
        object_geom[1] = deltaX
        object_geom[2] = deltaY
        object_geom[3] = deltaX2
        object_geom[4] = deltaY2
    if type == "triangle":
        """object_geom[3] += deltaX
        object_geom[4] += deltaY
        object_geom[5] += deltaX
        object_geom[6] += deltaY"""

def rotate_point(centerX, centerY, angle, posX, posY):
  s = math.sin(angle)
  c = math.cos(angle)

  #translate point back to origin:
  posX -= centerX
  posY -= centerY

  #rotate point
  xnew = posX * c - posY * s
  ynew = posX * s + posY * c

  #translate point back:
  posX = xnew + centerX
  posY = ynew + centerY
  return posX, posY
		
@addToClass(AST.MoveNode)
def execute(self):
    element = objects.get(self.children[0].tok)
    move_x = self.children[1].execute()
    move_y = self.children[2].execute()
    element.add_move(move_x, move_y)
	
@addToClass(AST.TickNode)
def execute(self):
    global tick
    tick = self.value.execute()

if __name__ == "__main__":
    import parserAnim
    import sys

    path = None
    if len(sys.argv) > 1:
        prog = sys.argv[1]
    else:
        path = "exemples/test_animaker2.txt"

    prog = open(path).read()
    ast = parserAnim.parse(prog)
    ast.execute()