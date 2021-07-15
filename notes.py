

def p_func(p): #func Bar (foo) foo + 10
    'expression : FUNCTION NAME LEFT_PAR NAME RIGHT_PAR expression'
    names[p[1]] = f'{p[2]}'

    func Bar (foo) foo + 10
    p[0] = [foo]
    p[1] = foo +10 #eval

    Bar(11)
    foo -> 11
    p[1]