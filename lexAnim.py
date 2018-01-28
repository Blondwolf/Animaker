import ply.lex as lex

reserved_words = (
    'while',
    'print',
    'move',
    'rotate',
    'Ball',
    'Rectangle',
	'Triangle',
    'PI',
	'tick',
	'screen',
	'translate'
)

tokens = (
    'IDENTIFIER',
	'INTEGER',
	'FLOAT',
	'COLOR',
    'ADD_OP',
    'MUL_OP'
) + tuple(map(lambda s: s.upper(), reserved_words))

literals = '();={},'

t_ADD_OP = r'[\+|-]'
t_MUL_OP = r'[/|\*]'
t_ignore = ' \t'

###       Tokens RegExp        ###

def t_IDENTIFIER(t):
    r'[a-zA-Z_]\w*'
    if t.value in reserved_words:   #La valeur des mots reservé devient leur types
        t.type = t.value.upper()
    return t
	
def t_INTEGER(t):
    r'[+-]?(?<!\.)\b[0-9]+\b(?!\.[0-9])'
    t.value = int(t.value)
    return t
	
def t_FLOAT(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value)
    return t
	
def t_COLOR(t):
    r'\[\d+,\s+\d+,\s+\d+\]'
    t.value = t.value
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lex.lex()

###       Main        ###

if __name__ == '__main__':
    import sys

    if len(sys.argv)>1:
        prog = open(sys.argv[1]).read()
    else:
        prog = open("exemples/test_final.txt").read()

    lex.input(prog)
    while 1:
        tok = lex.token()
        if not tok: break
        print("line %d: %s(%s)" % (tok.lineno, tok.type, tok.value))


