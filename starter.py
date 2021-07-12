from ply import lex
from ply import yacc
import pdb

debug = True

# -----------------------------------------------------------------------------
# calc.py
#
# A simple calculator with variables.
# -----------------------------------------------------------------------------

tokens = (
    'NAME','NUMBER',
    'EQUALS', 'ADD',
    'SUB', 'MULTIPLE',
    'DIVISION', 'LPAREN', 'RPAREN', 'DEF', 'FOR', 'TO', 'RUN'
    )

# Tokens
t_NAME    = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_EQUALS  = r'='
t_ADD     = r'\+'
t_SUB     = r'-'
t_MULTIPLE = r'\*'
t_DIVISION = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_DEF = r'def'
t_FOR = r'for'
t_TO  = r'to'
t_RUN = r'run'

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
precedence = (
    ('left','ADD','SUB'),
    ('left','MULTIPLE','DIVISION')
    # ('right','UMINUS'),
)

# dictionary of names (for storing variables)
names = { }
functions = { }

def p_statement_function(p):
    'statement : DEF '
    functions[p[1]] = p[3]
    
def p_expression_for(p):
    'expression : FOR NUMBER TO NUMBER RUN expression'  
    for e in range(p[2], p[4]):
        print(p[6])

def p_statement_assign(p):
    'statement : NAME EQUALS expression'
    names[p[1]] = p[3]

def p_statement_expr(p):
    'statement : expression'
    if p[1] != None:
        print(p[1])

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = p[1]

def p_expression_name(p):
    'expression : NAME'
    try:
        if p[1] == 'q' or p[1] == 'quit': quit()
        p[0] = names[p[1]]
    except LookupError:
        print(f"Undefined name {p[1]!r}")

def p_error(p):
    print(f"Syntax error at {p.value!r}")

def p_expression_parenthization(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_statement_multiple(p):
    'expression : expression MULTIPLE expression'
    p[0] = p[1] * p[3]

def p_statement_division(p):
    'expression : expression DIVISION expression'
    try:
        p[0] = p[1] / p[3]
    except ZeroDivisionError:
        print("You cannot divide by zero")

def p_statement_add(p):
    'expression : expression ADD expression'
    p[0] = p[1] + p[3]

def p_statement_sub(p):
    'expression : expression SUB expression'
    p[0] = p[1] - p[3]

import ply.yacc as yacc
yacc.yacc()

while True:
    try:
        s = input('calc > ')
    except EOFError:
        break
    yacc.parse(s)
