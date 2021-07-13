from ply import lex
from ply import yacc

debug = True

# -----------------------------------------------------------------------------
# calc.py
#
# A simple calculator with variables.
# -----------------------------------------------------------------------------

keywords = (
    'function',
    )

tokens = keywords + (
    'NAME','NUMBER',
    'ASSIGNMENT',
    'OPERATOR',
    )

# Tokens
#t_NAME        = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_ASSIGNMENT  = r'='
t_OPERATOR    = r'[+\-*/^%]'
t_function    = r'function'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_NAME(t):
    r'[a-zA-Z_]+'
    print(t.value, t.type)
    if t.value in keywords:
        t.type = t.value
    print(t)
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

class Scope:
    def __init__(self):
        self.names = {}
        self.loop_counter = 0
        self.loop_statements = []

class Interpreter:
    def __init__(self):
        self.stack = []
        self.push_scope()

    def eval(self, node):
        operation = node[0]

        if operation == "eval":
            return self.eval(node[1])
        elif operation == "assign":
            return self.assign_value(node[1], self.eval(node[2]))
        elif operation == "number":
            return node[1]
        elif operation == "lookup":
            return self.variable_value(node[1])
        elif operation == "binary_operation":
            return self.perform_operation(node[1], self.eval(node[2]), self.eval(node[3]))



    def assign_value(self, name, value):
        self.current_scope().names[name] = value
        return value

    def expression_number(self, number):
        return(number)

    def variable_value(self, name):
        try:
            return(self.current_scope().names[name])
        except LookupError:
            print(f"Undefined name {name}")
            return None

    def push_scope(self):
        scope = Scope()
        self.stack.append(scope)

    def current_scope(self):
        return(self.stack[-1])

    def perform_operation(self, operator, a, b):
        if operator == '+': return(a + b)
        if operator == '-': return(a - b)
        if operator == '*': return(a * b)
        if operator == '/': return(a / b)
        if operator == '^': return(a ** b)
        if operator == '%': return(a % b)

    def start_function(self, name, **parameter_list):
        pass

# dictionary of names (for storing variables)
interpreter = Interpreter()

def p_statement_assign(p):
    'statement : NAME ASSIGNMENT expression'
    p[0] = ("assign", p[1], p[3])

def p_statement_expr(p):
    'statement : expression'
    p[0] = ("eval", p[1])

def p_expression_function(p):
    'expression : function'
    p[0] = ("function", p[1])

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = ("number", p[1])

def p_expression_name(p):
    'expression : NAME'
    if p[1] == 'quit':
        quit()
    p[0] = ("lookup", p[1])

def p_expression_operation(p):
    'expression : expression OPERATOR expression'
    p[0] = ("binary_operation", p[2], p[1], p[3])

def p_error(p):
    print(f"Syntax error at {p.value!r}")

import ply.yacc as yacc
yacc.yacc()

while True:
    try:
        s = input('calc > ')
    except EOFError:
        break
    parse_tree = yacc.parse(s)
    print(parse_tree)
    result = interpreter.eval(parse_tree)
    print(result)
