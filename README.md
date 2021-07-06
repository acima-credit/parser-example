# parser-example
A framework to demonstrate the basics of programming language lexing and parsing.

This project uses code from (PLY)(https://github.com/dabeaz/ply) (Python Lex-Yacc) to build the foundation of a language interpreter.


To begin, install python 3. You may have it installed on your system already as `python3`.

This project is pure python and has no external dependencies to install.

To run the example script, run
```
python starter.py
```

You will be placed into an interactive console where you can define variables and print them out.

For example,
```
$ python starter.py
calc > my_number = 42
calc > my_number
42
```

You can toggle debug output (which is on by default) by setting the `debug` value near the top of starter.py.

To escape the console, use ctrl-c.

In the `ply` project, methods beginning with `p_` are given special handling as parsers. They require a [docstring](https://www.python.org/dev/peps/pep-0257/#id17) to document what will be parsed, and python code to handle the incoming parsed token object.

To add a new language feature, consider adding a new `p_*` method and experimenting.
