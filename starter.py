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
t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_ASSIGNMENT     = r'[=]'
t_ADDITION       = r'[+]'
t_SUBTRACTION    = r'[-]'
t_MULTIPLICATION = r'[*]'
t_DIVISION       = r'[/]'
t_EXPONENTIATION = r'\^'
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
            return self.get_value(node[1])
        elif operation == 'function':
            return self.store_function(node[1], node[2], node[3])
        elif operation == "add":
            return self.add(self.eval(node[1]), self.eval(node[2]))
        elif operation == 'subtract':
            return self.subtract(self.eval(node[1]), self.eval(node[2]))
        elif operation == 'multiply':
            return self.multiply(self.eval(node[1]), self.eval(node[2]))
        elif operation == 'divide':
            return self.divide(self.eval(node[1]), self.eval(node[2]))
        elif operation == 'exponentiate':
            return self.exponentiate(self.eval(node[1]), self.eval(node[2]))
        elif operation == 'mod':
            return self.mod(self.eval(node[1]), self.eval(node[2]))

    def assign_value(self, name, value):
        self.current_scope().names[name] = value
        return value

    def expression_number(self, number):
        return(number)

    def get_value(self, name):
        try:
            value = self.current_scope().names[name]
            if type(value) == int:
                return value
            else:
                return self.eval(value)
        except LookupError:
            print(f"Undefined name {name}")
            return None

    def push_scope(self):
        scope = Scope()
        self.stack.append(scope)

    def current_scope(self):
        return(self.stack[-1])

    def store_function(self, function_name, param_name, expression):
        scope = Scope()
        self.current_scope().names[function_name] = expression
        return function_name

    def add(self, x, y):
        return x + y

    def subtract(self, x, y):
        return x - y

    def multiply(self, x, y):
        return x * y

    def divide(self, x, y):
        return x / y

    def exponentiate(self, x, y):
        return x ** y

    def mod(self, x, y):
        return x % y

    def start_function(self, name, **parameter_list):
        pass

interpreter = Interpreter()

def p_statement_assign(p):
    'statement : NAME ASSIGNMENT expression'
    p[0] = ('assign', p[1], p[3])

def p_statement_expr(p):
    'statement : expression'
    p[0] = ('eval', p[1])

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = ('number', p[1])

def p_expression_name(p):
    'expression : NAME'
    if p[1] == 'q' or p[1] == 'quit' or p[1] == 'exit': quit()
    try:
        p[0] = ('lookup', p[1])
    except LookupError:
        print(f"Undefined name {p[1]!r}")
        p[0] = 0

def p_error(p):
    print(f"Syntax error at {p.value!r}")

def p_expression_parentheses(p):
    'expression : LPAREN expression RPAREN'
    p[0] = ('eval', p[2])

def p_function(p):
    'expression : NAME LPAREN NAME RPAREN FUNCTION expression'
    p[0] = ('function', p[1], p[3], p[6])

# def p_function_call(p):
#     'expression : NAME LPAREN NUMBER RPAREN'
#     # apple(5)

def p_expression_addition(p):
    'expression : expression ADDITION expression'
    p[0] = ('add', p[1], p[3])

def p_expression_subtraction(p):
    'expression : expression SUBTRACTION expression'
    p[0] = ('subtract', p[1], p[3])

def p_expression_multiplication(p):
    'expression : expression MULTIPLICATION expression'
    p[0] = ('multiply', p[1], p[3])

def p_expression_division(p):
    'expression : expression DIVISION expression'
    try:
        p[0] = ('divide', p[1], p[3])
    except ZeroDivisionError:
        print('Division by Zero')

def p_expression_exponentiation(p):
    'expression : expression EXPONENTIATION expression'
    p[0] = ('exponentiate', p[1], p[3])

def p_expression_modulo(p):
    'expression : expression MODULO expression'
    p[0] = ('mod', p[1], p[3])

import ply.yacc as yacc
yacc.yacc()

while True:
    try:
        s = input('calc> ')
    except EOFError:
        break
    parse_tree = yacc.parse(s)
    print(parse_tree)
    result = interpreter.eval(parse_tree)
    print(result)
