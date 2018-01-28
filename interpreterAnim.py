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

vars={}
objects={}

def write_exit(indent_level):
    str_indent = get_indent(indent_level)
    file.write("{}for event in pygame.event.get():\n".format(str_indent))
    file.write("{}    if event.type == QUIT:\n".format(str_indent))
    file.write("{}        sys.exit(0)\n".format(str_indent))

def write_refresh_func():
    file.write("def refresh_screen(objects, pygame, screen):\n")
    file.write("    for obj in objects:\n")
    file.write("        obj.draw(pygame, screen)\n\n")
	
def write_moves():
    file.write("        for obj in objects:\n")
    file.write("            obj.move()\n")
    file.write("            obj.draw(pygame, screen)\n")
    write_refresh_screen(12)
	
def write_header():
    file.write("import pygame, time, sys\n")
    file.write("from pygame.locals import *\n")
    file.write("from pygame.locals import QUIT, MOUSEBUTTONDOWN, KEYDOWN, K_RETURN\n")
    file.write("from models.ball import Ball\n")
    file.write("from models.triangle import Triangle\n")
    file.write("from models.rectangle import Rectangle\n\n")

    write_refresh_func()
	
    file.write("if __name__ == '__main__':\n")
    file.write("    pygame.init()\n")
    file.write("    objects=[]\n")
	
def write_footer():
    file.write("    pygame.display.flip()\n")
    file.write("    running = 1\n")
    file.write("    while running:\n")
    file.write("        for event in pygame.event.get():\n")
    file.write("            if event.type == QUIT:\n")
    file.write("                running = 0\n")

def get_indent(indent_level):
    str_indent = ""
    for i in range(indent_level):
        str_indent += " "
    return str_indent

def write_refresh_screen(indent_level=0):
    str_indent = get_indent(indent_level)
    file.write("{}refresh_screen(objects, pygame, screen)\n".format(str_indent))
    file.write("{}pygame.display.update()\n".format(str_indent))
    file.write("{}time.sleep(tick/1000)\n".format(str_indent))

@addToClass(AST.ProgramNode)
def execute(self, indent_level=0):
    global file
    global objects
    global tick
    global screen_define
    screen_define = False
    tick=100# default
    file = open("test.py", 'w')
    write_header()
    indent_level = 4
    for c in self.children:
        c.execute(indent_level)
    if not screen_define:
        file.write("    screen = pygame.display.set_mode((800, 600))\n")
    write_footer()
    write_moves()
    file.close()
    
@addToClass(AST.TokenNode)
def execute(self, indent_level=0):
    if isinstance(self.tok, str):
        try:
            return vars[self.tok]
        except KeyError:
            print("*** Error: variable %s undefined!" % self.tok)
    return self.tok
	
@addToClass(AST.ElementNode)
def execute(self, indent_level=0):
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
        element = "Ball({}, {}, {}, {})\n".format(self.tok[1], self.tok[2], self.tok[3], color)
    elif object_type == "rectangle":
        if length == 6:
            color = self.tok[5]
        element = "Rectangle({}, {}, {}, {}, {})\n".format(self.tok[1], self.tok[2], self.tok[3], self.tok[4], color)
    elif object_type == "triangle":
        if length == 8:
            color = self.tok[7]
        element = "Triangle({}, {}, {}, {}, {}, {}, {})\n".format(self.tok[1], self.tok[2], self.tok[3], self.tok[4], self.tok[5], self.tok[6], color)
    return element

@addToClass(AST.OpNode)
def execute(self, indent_level=0):
    args = [c.tok for c in self.children]
    return "{} {} {}".format(args[0], self.op, args[1])

@addToClass(AST.AssignNode)
def execute(self, indent_level=0):
    str_indent = get_indent(indent_level)
    file.write("{}{} = {}".format(str_indent, self.children[0].tok, self.children[1].execute()))
    if self.children[1].type == "element":
        objects[self.children[0].tok] = self.children[1].execute(indent_level)
        file.write("{}objects.append({})\n".format(str_indent, self.children[0].tok))
    else:
        vars[self.children[0].tok] = self.children[1].execute(indent_level)

@addToClass(AST.PrintNode)
def execute(self, indent_level=0):
    str_indent = get_indent(indent_level)
    file.write("{}print({})\n".format(str_indent, self.children[0].tok))
    
@addToClass(AST.WhileNode)
def execute(self, indent_level=0):
    str_indent = get_indent(indent_level)
    file.write("{}{}({}):\n".format(str_indent, self.type, self.children[0].tok))
    file.write("{}    screen.fill(0)\n".format(str_indent))
    for c in self.children[1].children:
        if isinstance(c, AST.OpNode):
            file.write("    {} = ".format(c))
        c.execute(indent_level + 4)
    write_refresh_screen(indent_level + 4)
    write_exit(indent_level + 4)

@addToClass(AST.IntNode)
def execute(self, indent_level=0):
    return self.value
	
@addToClass(AST.FloatNode)
def execute(self, indent_level=0):
    return self.value
		
@addToClass(AST.RotateNode)
def execute(self, indent_level=0):
    str_indent = get_indent(indent_level)
    element = objects.get(self.children[0].tok)
    alpha = self.children[1].execute()
    file.write("{}{}.rotate({}, {})\n".format(str_indent, self.children[0].tok, alpha))
    file.write("{}{}.draw(pygame, screen)\n".format(str_indent, self.children[0].tok))

@addToClass(AST.MoveNode)
def execute(self, indent_level=0):
    str_indent = get_indent(indent_level)
    element = objects.get(self.children[0].tok)
    move_x = self.children[1].execute()
    move_y = self.children[2].execute()
    file.write("{}{}.add_move({}, {})\n".format(str_indent, self.children[0].tok, move_x, move_y))
	
@addToClass(AST.TranslateNode)
def execute(self, indent_level=0):
    element = objects.get(self.children[0].tok)
    translate_x = self.children[1].execute()
    translate_y = self.children[2].execute()
    str_indent = get_indent(indent_level)
    file.write("{}{}.translate({}, {})\n".format(str_indent, self.children[0].tok, translate_x, translate_y))
    file.write("{}{}.draw(pygame, screen)\n".format(str_indent, self.children[0].tok))
	
@addToClass(AST.TickNode)
def execute(self, indent_level=0):
    if indent_level > 4: # tick should define in begin of program
        return
    str_indent = get_indent(indent_level)
    file.write("{}tick={}\n".format(str_indent, self.value.execute()))
	
@addToClass(AST.ScreenNode)
def execute(self, indent_level=0):
    if indent_level > 4: # screen should define in begin of program
        return
    str_indent = get_indent(indent_level)
    screen_define = True
    file.write("{}screen = pygame.display.set_mode(({}, {}))\n".format(str_indent, self.children[0].execute(), self.children[1].execute()))

if __name__ == "__main__":
    import parserAnim
    import sys

    path = None
    if len(sys.argv) > 1:
        prog = sys.argv[1]
    else:
        path = "exemples/test_final.txt"

    prog = open(path).read()
    ast = parserAnim.parse(prog)
    ast.execute()