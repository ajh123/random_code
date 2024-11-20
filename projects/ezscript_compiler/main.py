from lexer import *
from errors import LexerError

with open("test.ezscript") as f:
    try:
        tokens = lexer(f.read())
        for token in tokens:
            print(token)
    except LexerError as e:
        print(e)
        sys.exit(-1)