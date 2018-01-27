import AST
from AST import addToClass
from functools import reduce

operations = {
    '+' : lambda x,y: x+y,
    '-' : lambda x,y: x-y,
    '*' : lambda x,y: x*y,
    '/' : lambda x,y: x/y,
}

vars ={}

def write_header():
    file.write("import pygame\n")
    file.write("from pygame.locals import *\n")
    file.write("from pygame.locals import QUIT, MOUSEBUTTONDOWN, KEYDOWN, K_RETURN\n")
    file.write("if __name__ == '__main__':\n")
    file.write("    pygame.init()\n")
    file.write("    screen = pygame.display.set_mode((640, 480))\n")
	
def write_footer():
    file.write("    pygame.display.flip()\n")
    file.write("    running = 1\n")
    file.write("    while running:\n")
    file.write("        for event in pygame.event.get():\n")
    file.write("            if event.type == QUIT:\n")
    file.write("                running = 0\n")


@addToClass(AST.ProgramNode)
def execute(self):
    global file
    file = open("test.py", 'w')
    write_header()
    for c in self.children:
        c.execute()
    write_footer()
    
@addToClass(AST.TokenNode)
def execute(self):
    if isinstance(self.tok, str):
        try:
            return vars[self.tok]
        except KeyError:
            print("*** Error: variable %s undefined!" % self.tok)
    return self.tok

@addToClass(AST.OpNode)
def execute(self):
    args = [c.execute() for c in self.children]
    if len(args) == 1:
        args.insert(0,0)
    return reduce(operations[self.op], args)

@addToClass(AST.AssignNode)
def execute(self):
    print(self.children[0].tok)
    vars[self.children[0].tok] = self.children[1].execute()

@addToClass(AST.PrintNode)
def execute(self):
    print(self.children[0].type)
    print (self.children[0].execute())
    
@addToClass(AST.WhileNode)
def execute(self):
    while self.children[0].execute():
        self.children[1].execute()
		
@addToClass(AST.ShowNode)
def execute(self):
    #file.write(self+"\n")
    #print(self.children)
    object_geom = vars.get(self.children[0].tok)
    type = object_geom[0].lower()
    if type == "ball":
        file.write("    pygame.draw.circle(screen, [0, 0, 255], ({}, {}), {})\n".format(int(object_geom[1]),
                                                                                        int(object_geom[2]),
                                                                                        int(object_geom[3])))
    elif type == "rectangle":
        file.write("    pygame.draw.rect(screen, [0, 0, 255], ({}, {}, {}, {}))\n".format(int(object_geom[1]),
                                                                                          int(object_geom[2]),
                                                                                          int(object_geom[3]),
                                                                                          int(object_geom[4])))
    elif type == "triangle":
        file.write("    pygame.draw.polygon(screen, [0, 0, 255], [({}, {}), ({}, {}), ({}, {})])\n".format(int(object_geom[1]),
                                                                                                           int(object_geom[2]),
                                                                                                           int(object_geom[3]),
                                                                                                           int(object_geom[4]),
                                                                                                           int(object_geom[5]),
                                                                                                           int(object_geom[6])))
		
@addToClass(AST.RotateNode)
def execute(self):
    pass
    #while self.children[0].execute():
    #    self.children[1].execute()
		
@addToClass(AST.MoveNode)
def execute(self):
    object_geom = vars.get(self.children[0].tok)
    type = object_geom[0].lower()
    deltaX = self.children[1].execute()
    deltaY = self.children[2].execute()

    #For all, moves 2 firsts vars
    object_geom[1] += deltaX
    object_geom[2] += deltaY

    #For triangle (or polygones) you need to move all coords
    if type == "triangle":
        object_geom[3] += deltaX
        object_geom[4] += deltaY
        object_geom[5] += deltaX
        object_geom[6] += deltaY

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