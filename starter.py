from ply import lex
from ply import yacc

debug = True

# -----------------------------------------------------------------------------
# calc.py
#
# A simple calculator with variables.
# -----------------------------------------------------------------------------

keywords = ()

tokens = keywords + (
    'NAME','NUMBER',
    'EQUALS', 'ADD',
    'SUBTRACT', 'MULTIPLY',
    'DIVIDE', 'MODULO',
    'EXPONENT', 'ARROW', 
    'LEFT_PAR','RIGHT_PAR',
    'FUNCTION'
    )

# Tokens
t_EQUALS    = r'='
t_ADD       = r'[+]'
t_SUBTRACT  = r'[-](?!>)'
t_MULTIPLY  = r'[*]'
t_DIVIDE    = r'[/]'
t_MODULO    = r'[%]'
t_EXPONENT  = r'[\^]'
t_ARROW     = r'->'
t_LEFT_PAR  = r'[(]'
t_RIGHT_PAR = r'[)]'
t_FUNCTION  = r'func'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    #print(t.value, t.type)
    if t.value in keywords:
        t.type = t.value
    #print(t)
    return t

# Ignored characters
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print(f"Illegal character {t.value[0]!r}")
    t.lexer.skip(1)

# Build the lexer
import ply.lex as lex
lex.lex(debug=debug)

# Precedence rules for the arithmetic operators
precedence = (
    ('left','ADD','SUBTRACT'),
    ('left','MULTIPLY','DIVIDE'),
    ('left','EXPONENT','MODULO'))

# dictionary of names (for storing variables)
names = { }

def p_statement_assign(p):
    'statement : NAME EQUALS expression'
    names[p[1]] = p[3]

def p_statement_expr(p):
    'statement : expression'
    print(p[1])

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = p[1]

def p_expression_name(p):
    'expression : NAME'
    if p[1] == 'q' or p[1] == 'quit' or p[1] == 'exit': quit()
    try:
        value = names[p[1]]
        if type(value) is int:  # why is this here
            p[0] = value
        elif type(value) is str:
            p[0] = eval(value)
    except LookupError:
        print(f"Undefined name {p[1]!r}")
        p[0] = 0

def p_expression_add(p):
    'expression : expression ADD expression'
    p[0] =p[1] + p[3]

def p_expression_subtract(p):
    'expression : expression SUBTRACT expression'
    p[0] =p[1] - p[3]

def p_expression_multiply(p):
    'expression : expression MULTIPLY expression'
    p[0] =p[1] * p[3]

def p_expression_divide(p):
    'expression : expression DIVIDE expression'
    p[0] =p[1] / p[3]

def p_expression_modulo(p):
    'expression : expression MODULO expression'
    p[0] =p[1] % p[3]

def p_expression_exponent(p):
    'expression : expression EXPONENT expression'
    p[0] =p[1] ** p[3]

def p_expression_parentheses(p):
    'expression : LEFT_PAR expression RIGHT_PAR'
    p[0] = p[2]

def p_lambda(p):
    'expression : NAME ARROW expression'
    names[p[1]] = f'{p[3]}'

def p_func(p): #func Bar (foo) foo + 10
    'expression : FUNCTION NAME LEFT_PAR NAME RIGHT_PAR expression'
    names[p[1]] = f'{p[2]}'

def p_func(p):# Bar(20)    : 30
    'expression : NAME LEFT_PAR NAME RIGHT_PAR' 

def p_func(p):# Bar()    : 30`
    'expression : NAME LEFT_PAR RIGHT_PAR' 

def p_error(p):
    print(f"Syntax error at {p.value!r}")

import ply.yacc as yacc
yacc.yacc()

while True:
    try:
        s = input('calc > ')
    except EOFError:
        break
    yacc.parse(s)
