import ply.yacc as yacc
from lexAnim import tokens
import AST

operations = {
    '+' : lambda x,y: x+y,
    '-' : lambda x,y: x-y,
    '/' : lambda x,y: x/y,
    '*' : lambda x,y: x*y,
}

vars = {}

precedence = (
    ('left', 'ADD_OP'),
    ('left', 'MUL_OP'),
    ('right', 'UMINUS'),
)

###     Expressions basic     ###

def p_expression_program(p):
    """program : statement ';'"""
    p[0] = AST.ProgramNode(p[1])

def p_expression_recursive(p):
    """program : statement ';' program"""
    p[0] = AST.ProgramNode([p[1]] + p[3].children)

def p_expression_statement(p):
    """statement : assignation
    | structure"""
    try:
        p[0] = p[2]
    except:
        p[0] = p[1]

def p_expression_print(p):
    """statement : PRINT expression"""
    p[0] = AST.PrintNode(p[2])

def p_expression_assignation(p):
    """assignation : IDENTIFIER '=' expression"""
    p[0] = AST.AssignNode([AST.TokenNode(p[1]), p[3]])

def p_expression_structure(p):
    """structure : WHILE expression '{' program '}'"""
    p[0] = AST.WhileNode([p[2], p[4]])

def p_expression_identifier(p):
    """expression : IDENTIFIER"""
    p[0] = AST.TokenNode(p[1])

def p_expression_num(p):
    """expression : type"""
    p[0] = AST.TokenNode(p[1])

def p_expression_addop(p):
    """expression : expression ADD_OP expression
    | expression MUL_OP expression"""
    p[0] = AST.OpNode(p[2], [p[1], p[3]])

def p_expression_parenthesis(p):
    """expression : '(' expression ')' """
    p[0] = p[2]

def p_expression_uminus(p):
    'expression : ADD_OP expression %prec UMINUS'
    p[0] = AST.OpNode(p[1], [p[2]])

def p_error(p):
    print("Syntax error in line %d" %p.lineno)
    yacc.errok()

###     Expressions Animaker     ###

def p_type_number(p):
    """type : INTEGER
    | FLOAT"""
    p[0] = AST.TypeNode(p[1])
	
def p_int_number(p):
    """int : INTEGER"""
    p[0] = AST.IntNode(p[1])
	
def p_float_number(p):
    """float : INTEGER"""
    p[0] = AST.FloatNode(p[1])

def p_expression_pi(p):
    """expression : PI"""
    p[0] = AST.FloatNode(3.1415926535)  #A voir !NUMBER? pas geré sinon comme un number

def p_expression_ball(p):
    """expression : BALL INTEGER ',' INTEGER ',' INTEGER
    | BALL INTEGER ',' INTEGER ',' INTEGER ',' COLOR"""
    if len(p) == 7:
        p[0] = AST.ElementNode([p[1], p[2], p[4], p[6]])
    elif len(p) == 9:
        p[0] = AST.ElementNode([p[1], p[2], p[4], p[6], p[8]])

def p_expression_rectangle(p):
    """expression : RECTANGLE INTEGER ',' INTEGER ',' INTEGER ',' INTEGER
    | RECTANGLE INTEGER ',' INTEGER ',' INTEGER ',' INTEGER ',' COLOR"""
    if len(p) == 9:
        p[0] = AST.ElementNode([p[1], p[2], p[4], p[6], p[8]])
    elif len(p) == 11:
        p[0] = AST.ElementNode([p[1], p[2], p[4], p[6], p[8], p[10]])
	
def p_expressiom_triangle(p):
    """expression : TRIANGLE INTEGER ',' INTEGER ',' INTEGER ',' INTEGER ',' INTEGER ',' INTEGER
    | TRIANGLE INTEGER ',' INTEGER ',' INTEGER ',' INTEGER ',' INTEGER ',' INTEGER ',' COLOR"""
    if len(p) == 13:
        p[0] = AST.ElementNode([p[1], p[2], p[4], p[6], p[8], p[10], p[12]])
    elif len(p) == 15:
        p[0] = AST.ElementNode([p[1], p[2], p[4], p[6], p[8], p[10], p[12], p[14]])

def p_expression_move(p):
    """statement : MOVE IDENTIFIER int int"""
    p[0] = AST.MoveNode([AST.TokenNode(p[2]), p[3], p[4]])

def p_expression_rotate(p):
    """statement : ROTATE IDENTIFIER float"""
    p[0] = AST.RotateNode([AST.TokenNode(p[2]), p[3]])

def p_expression_show(p):
    """statement : SHOW expression"""
    p[0] = AST.ShowNode(p[2])
	
def p_expression_tick(p):
    """statement : TICK int"""
    p[0] = AST.TickNode(p[2])

###     Yacc and decorator      ###

def exp_decorator(decorated_func):
    def wrapper_expression_decorator(*args):
        print("deco : ", args)
        decorated_func(*args)
    return wrapper_expression_decorator

def parse(program, debug=0):
	return yacc.parse(program, debug)

yacc.yacc(outputdir='generated')

###       Main        ###

if __name__ == '__main__':
    import sys

    path = ""
    if len(sys.argv)>1:
        prog = sys.argv[1]
    else:
        path = "exemples/test_final.txt"

    if path is not None:
        prog = open(path).read()
        result = parse(prog) #debug=1
        #In console
        print(result)

        #In PDF
        import os
        graph = result.makegraphicaltree()
        name = os.path.splitext(path)[0]+"-ast.pdf"
        graph.write_pdf(name)
        print("wrote ast to", name)