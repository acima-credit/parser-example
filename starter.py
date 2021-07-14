from ply import lex
from ply import yacc
debug = True
# -----------------------------------------------------------------------------
# calc.py
#
# A simple calculator with variables.
# -----------------------------------------------------------------------------
tokens = (
    'FUNCTION',
    'NAME',
    'NUMBER',
    'ASSIGNMENT',
    'ADDITION',
    'SUBTRACTION',
    'MULTIPLICATION',
    'DIVISION',
    'EXPONENTIATION',
    'MODULO',
    'LPAREN',
    'RPAREN'
    )

# Tokens
t_FUNCTION = r'~\>'
t_NAME    = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_ASSIGNMENT     = r'[=]'
t_ADDITION       = r'[+]'
t_SUBTRACTION    = r'[-]'
t_MULTIPLICATION = r'[*]'
t_DIVISION       = r'[/]'
t_EXPONENTIATION = r'[^]'
t_MODULO         = r'[%]'
t_LPAREN         = r'[(]'
t_RPAREN         = r'[)]'

def t_NUMBER(t):
    r'-?\d+'
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
    ('left', 'ADDITION', 'SUBTRACTION'),
    ('left', 'MULTIPLICATION', 'DIVISION', 'MODULO'),
    ('left', 'EXPONENTIATION')
)

# dictionary of names (for storing variables)
names = { }

def p_statement_assign(p):
    'statement : NAME ASSIGNMENT expression'
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
        p[0] = names[p[1]]
    except LookupError:
        print(f"Undefined name {p[1]!r}")
        p[0] = 0

def p_error(p):
    print(f"Syntax error at {p.value!r}")

def p_expression_parentheses(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_lambda(p):
    'expression : NAME LPAREN NAME RPAREN FUNCTION expression'
    names[p[1]] = f'{p[6]}'

def p_expression_addition(p):
    'expression : expression ADDITION expression'
    p[0] = p[1] + p[3]

def p_expression_subtraction(p):
    'expression : expression SUBTRACTION expression'
    p[0] = p[1] - p[3]

def p_expression_multiplication(p):
    'expression : expression MULTIPLICATION expression'
    p[0] = p[1] * p[3]

def p_expression_division(p):
    'expression : expression DIVISION expression'
    try:
        p[0] = p[1] / p[3]
    except ZeroDivisionError:
        print('Division by Zero')

def p_expression_exponentiation(p):
    'expression : expression EXPONENTIATION expression'
    p[0] = p[1] ** p[3]

def p_expression_modulo(p):
    'expression : expression MODULO expression'
    p[0] = p[1] % p[3]

import ply.yacc as yacc
yacc.yacc()

while True:
    try:
        s = input('calc> ')
    except EOFError:
        break
    yacc.parse(s)
