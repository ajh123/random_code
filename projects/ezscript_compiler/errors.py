from typing import List
from tokens import Token

class LexerError(Exception):
    def __init__(self, message: str, line: int, col: int, source: str, length: int = 1):
        self.message = message
        self.line = line
        self.col = col
        self.source = source
        self.length = length
        super().__init__(message)

    def __str__(self):
        lines = self.source.splitlines()
        error_line = lines[self.line - 1] if self.line - 1 < len(lines) else ""
        pointer = " " * (self.col - 1) + "^" * self.length
        return (
            f"  File \"<stdin>\", line {self.line}\n"
            f"    {error_line}\n"
            f"    {pointer}\n"
            f"LexerError: {self.message}"
        )


def raise_lexer_error(message: str, source: str, pos: int, length: int = 1):
    lines = source[:pos + 1].splitlines()
    line = len(lines)
    col = len(lines[-1])
    raise LexerError(message, line, col, source, length)


class ParserError(Exception):
    def __init__(self, message: str, pos: int, tokens: List[Token], source: str):
        self.message = message
        self.pos = pos
        self.tokens = tokens
        self.source = source
        super().__init__(message)

    def __str__(self):
        if self.pos < len(self.tokens):
            token = self.tokens[self.pos]
            # Calculate the start index of the token in the source string
            token_start_index = sum(len(t.value) for t in self.tokens[:self.pos])

            # Split the source into lines
            lines = self.source.splitlines()
            
            # Count the lines up to the token's starting index
            token_line = 0
            char_count = 0
            for i, line in enumerate(lines):
                char_count += len(line) + 1  # +1 for the newline character
                if char_count > token_start_index:
                    token_line = i + 1  # +1 for 1-based index
                    break
            
            # Calculate the column number (position of the token within the line)
            token_line_start = sum(len(line) + 1 for line in lines[:token_line - 1])  # Sum up the length of lines before this one
            token_col = token_start_index - token_line_start + 1

            # Get the error line and pointer
            error_line = lines[token_line - 1] if token_line - 1 < len(lines) else ""
            pointer = " " * (token_col - 1) + "^" * len(token.value)  # Pointer for the token position

            return (
                f"  File \"<stdin>\", line {token_line}\n"
                f"    {error_line}\n"
                f"    {pointer}\n"
                f"ParseError: {self.message}"
            )
        else:
            return f"ParseError: {self.message}"

def raise_parser_error(message: str, tokens: List[Token], pos: int, source: str):
    raise ParserError(message, pos, tokens, source)

