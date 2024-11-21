from typing import List
from errors import *
from tokens import *

def lexer(data: str) -> List[TokenWithPos]:
    pos = 0
    char = data[pos]
    tokens: List[TokenWithPos] = []

    while pos < len(data):
        while char in ["\t", "\n", " "]:
            pos += 1
            try: char = data[pos]
            except: char = ""

        if (char.isalnum() or char == ".") and not char.isdigit():
            id_str = ""
            start_pos = pos
            while char.isalnum() or char == ".":
                id_str += char
                pos += 1
                try: char = data[pos]
                except: char = ""
            
            if id_str in keywords.keys():
                tokens.append(TokenWithPos(keywords[id_str], start_pos, pos))
            elif id_str in primitives.keys():
                tokens.append(TokenWithPos(primitives[id_str], start_pos, pos))
            else:
                tokens.append(TokenWithPos(Identifier(id_str), start_pos, pos))

        elif char.isdigit() or (char == "." and pos + 1 < len(data) and data[pos + 1].isdigit()):
            num_str = ""
            dot_count = 0
            start_pos = pos
            if isinstance(tokens[len(tokens) - 1].token, Operator) and tokens[len(tokens) - 1].token.value == "-":
                if data[pos - 1] == "-":
                    num_str = "-" + num_str
                    del tokens[len(tokens) - 1]
            
            while char.isdigit() or char == ".":
                if char == ".": dot_count += 1
                num_str += char
                pos += 1
                try: char = data[pos]
                except: char = ""
            
            if dot_count > 1:
                raise_lexer_error(f"The number `{num_str}` contains multiple dots!", data, start_pos, pos - start_pos)
            elif dot_count == 1:
                tokens.append(TokenWithPos(Literal(num_str, primitives["float"]), start_pos, pos))
            else:
                tokens.append(TokenWithPos(Literal(num_str, primitives["int"]), start_pos, pos))

        elif char in ["\"", "'"]:
            op = char
            value_str = ""
            start_pos = pos
            pos += 1
            char = data[pos] if pos < len(data) else ""

            while char != op:
                if pos >= len(data):
                    raise_lexer_error(f"Unterminated string literal. HINT: add `{op}` on the end!", data, start_pos, pos - start_pos)
                if char == "\n":
                    raise_lexer_error(f"Unterminated string literal. HINT: add `{op}` on the end!", data, start_pos, pos - start_pos)
                value_str += char
                pos += 1
                char = data[pos] if pos < len(data) else ""

            pos += 1
            char = data[pos] if pos < len(data) else ""

            tokens.append(TokenWithPos(Literal(value_str, primitives["string"]), start_pos, pos))
        elif char in operators:
            pos += 1
            op_str = char
            try: char = data[pos]
            except: char = ""

            tokens.append(TokenWithPos(operators[op_str], pos, pos))
        else:
            raise_lexer_error(f"Unknown character `{char}`.", data, pos)

    return tokens
