import AST
from AST import addToClass
from functools import reduce
from models.ball import Ball
from models.rectangle import Rectangle
from models.triangle import Triangle
import os
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
	
def check_screen(children):
    for c in children:
        if isinstance(c, AST.ScreenNode):
            return True
    return False

@addToClass(AST.ProgramNode)
def execute(self, indent_level=0):
    global file
    global objects
    global tick
    tick=100# default
    file = open("test.py", 'w')
    write_header()
    if not check_screen(self.children):
        file.write("    screen = pygame.display.set_mode((800, 600))\n")
    indent_level = 4
    for c in self.children:
        c.execute(indent_level)
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

@addToClass(AST.OpNode)
def execute(self, indent_level=0):
    args = []
    for c in self.children:
        if isinstance(c, AST.FloatNode) or isinstance(c, AST.IntNode):
            args.append(c.execute())
        else:
            args.append(c.tok)
    return "{} {} {}".format(args[0], self.op, args[1])

@addToClass(AST.AssignNode)
def execute(self, indent_level=0):
    str_indent = get_indent(indent_level)
    file.write("{}{} = {}\n".format(str_indent, self.children[0].tok, self.children[1].execute()))
    c_type = self.children[1].type
    if c_type == "ball" or c_type == "rectangle" or c_type == "triangle":
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
	
@addToClass(AST.ColorNode)
def execute(self, indent_level=0):
    return self.value
	
@addToClass(AST.BallNode)
def execute(self, indent_level=0):
    args = [self.children[i].execute() for i in range(1, len(self.children))]
    if len(args) == 3:
        args.append([255, 255, 255]) # default value color white
    return "Ball({}, {}, {}, {})\n".format(*args)
	
@addToClass(AST.RectangleNode)
def execute(self, indent_level=0):
    args = [self.children[i].execute() for i in range(1, len(self.children))]
    if len(args) == 4:
        args.append([255, 255, 255]) # default value color white
    return "Rectangle({}, {}, {}, {}, {})\n".format(*args)
	
@addToClass(AST.TriangleNode)
def execute(self, indent_level=0):
    args = [self.children[i].execute() for i in range(1, len(self.children))]
    if len(args) == 6:
        args.append([255, 255, 255]) # default value color white
    return "Triangle({}, {}, {}, {}, {}, {}, {})\n".format(*args)
		
@addToClass(AST.RotateNode)
def execute(self, indent_level=0):
    str_indent = get_indent(indent_level)
    element = objects.get(self.children[0].tok)
    alpha_node = self.children[1].execute()
    if isinstance(alpha_node, AST.TokenNode):
        alpha = alpha_node.execute()
    else:
        alpha = alpha_node
    file.write("{}{}.rotate({})\n".format(str_indent, self.children[0].tok, alpha))
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
    os.system("test.py")