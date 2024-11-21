from lexer import *
from parser import Parser
from errors import LexerError, ParserError
import sys

file = sys.argv[1]

with open(file) as f:
    source = f.read()
    try:
        # First, use the lexer to tokenize the source code
        tokens = lexer(source)

        for token in tokens:
            print(token)
        
        print("=====")
        
        # Then, pass the tokens to the parser
        parser = Parser(tokens, source)  # Instantiate the Parser with the tokens
        ast = parser.parse()  # Parse the tokens and generate the AST
        
        # Print the resulting Abstract Syntax Tree (AST)
        print(ast)

    except LexerError as e:
        e.file = file
        print(e)
        sys.exit(-1)

    except ParserError as e:
        e.file = file
        print(e)
        sys.exit(-1)
