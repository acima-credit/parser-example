from ply import lex
from ply import yacc

debug = True

# -----------------------------------------------------------------------------
# calc.py
#
# A simple calculator with variables.
# -----------------------------------------------------------------------------

tokens = (
    'NAME','NUMBER',
    'EQUALS', 'MATH', 'ARROW', 
    )

# Tokens
t_NAME    = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_EQUALS  = r'='
t_MATH    = r'(\*{2})|([\+\-\*\/\%])'
t_ARROW   = r'&'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
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
precedence = ()

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
    if p[1] == 'q' or p[1] == 'quit': quit()
    try:
        value = names[p[1]]
        if type(value) is int:
            p[0] = value
        elif type(value) is str:
            p[0] = eval(value) 
    except LookupError:
        print(f"Undefined name {p[1]!r}")
        p[0] = 0

def p_expression_math(p):
    'expression : expression MATH expression'
    p[0] = eval(f'{p[1]}{p[2]}{p[3]}') 	

def p_lambda(p):
    'expression : NAME ARROW NUMBER MATH NUMBER'
    names[p[1]] = f'{p[3]}{p[4]}{p[5]}'

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
